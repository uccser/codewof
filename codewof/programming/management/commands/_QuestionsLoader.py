"""Custom loader for loading programming questions."""

from os.path import join
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from utils.TranslatableModelLoader import TranslatableModelLoader
from utils.errors import (
    MissingRequiredFieldError,
    InvalidYAMLValueError,
    KeyNotFoundError
)
from utils.language_utils import get_available_languages
from programming.models import (
    QuestionTypeProgram,
    QuestionTypeProgramTestCase,
    QuestionTypeFunction,
    QuestionTypeFunctionTestCase,
    QuestionTypeParsons,
    QuestionTypeParsonsTestCase,
    QuestionTypeDebugging,
    QuestionTypeDebuggingTestCase,
    DifficultyLevel,
    ProgrammingConcepts,
    QuestionContexts
)

VALID_QUESTION_TYPES = {
    QuestionTypeProgram.QUESTION_TYPE: {
        'question_class': QuestionTypeProgram,
        'test_case_class': QuestionTypeProgramTestCase,
    },
    QuestionTypeFunction.QUESTION_TYPE: {
        'question_class': QuestionTypeFunction,
        'test_case_class': QuestionTypeFunctionTestCase,
    },
    QuestionTypeParsons.QUESTION_TYPE: {
        'question_class': QuestionTypeParsons,
        'test_case_class': QuestionTypeParsonsTestCase,
    },
    QuestionTypeDebugging.QUESTION_TYPE: {
        'question_class': QuestionTypeDebugging,
        'test_case_class': QuestionTypeDebuggingTestCase,
    },
}
VALID_QUESTION_TYPE_SETS = [
    {
        QuestionTypeFunction.QUESTION_TYPE, QuestionTypeParsons.QUESTION_TYPE
    },
]
TEST_CASE_FILE_TEMPLATE = 'test-case-{id}-{type}.txt'


class QuestionsLoader(TranslatableModelLoader):
    """Custom loader for loading questions."""

    @transaction.atomic
    def load(self):
        """Load questions.

        Raise:
            MissingRequiredFieldError: when no object can be found with the matching
                attribute.
        """
        questions_structure = self.load_yaml_file(self.structure_file_path)

        for (question_slug, question_data) in questions_structure.items():
            if 'type' in question_data:
                question_types = [question_data['type']]
            elif 'types' in question_data:
                question_types = question_data['types']
            else:
                raise MissingRequiredFieldError(
                    self.structure_file_path,
                    [
                        'types/types',
                    ],
                    'Question'
                )

            # Check question types are valid
            for question_type in question_types:
                if question_type not in VALID_QUESTION_TYPES.keys():
                    raise InvalidYAMLValueError(
                        self.structure_file_path,
                        'type',
                        'One of {}'.format(VALID_QUESTION_TYPES.keys())
                    )
                if len(question_types) > 1:
                    if set(question_types) not in VALID_QUESTION_TYPE_SETS:
                        raise InvalidYAMLValueError(
                            self.structure_file_path,
                            'types',
                            'Invalid pairing of types, must be one of {}'.format(VALID_QUESTION_TYPE_SETS)
                        )

            # Check test cases exist
            try:
                question_test_cases = question_data['test-cases']
            except KeyError:
                raise MissingRequiredFieldError(
                    self.structure_file_path,
                    [
                        'test-cases',
                    ],
                    'Question'
                )

            question_translations = self.get_blank_translation_dictionary()

            # Read title and question text
            content_filename = join(question_slug, 'question.md')
            content_translations = self.get_markdown_translations(content_filename)
            for language, content in content_translations.items():
                question_translations[language]['title'] = content.title
                question_translations[language]['question_text'] = content.html_string

            # Read solution
            solution_filename = join(question_slug, 'solution.py')
            for language in get_available_languages():
                solution = open(self.get_localised_file(language, solution_filename), encoding='UTF-8').read()
                question_translations[language]['solution'] = solution
                if question_type == QuestionTypeParsons.QUESTION_TYPE:
                    lines = clean_parsons_lines(solution.split('\n'))
                    extra_lines = question_data.get('parsons-extra-lines', [])
                    lines += clean_parsons_lines(extra_lines)
                    lines_as_text = '\n'.join(lines)
                    question_translations[language]['lines'] = lines_as_text

            # If debugging question, get initial code,
            if QuestionTypeDebugging.QUESTION_TYPE in question_types:
                initial_code_filename = join(question_slug, 'initial.py')
                for language in get_available_languages():
                    initial_code = open(self.get_localised_file(
                        language, initial_code_filename), encoding='UTF-8').read()
                    question_translations[language]['initial_code'] = initial_code
            
            if "difficulty" in question_data:
                difficulty_slug = question_data['difficulty']
                try:
                    difficulty_level = DifficultyLevel.objects.get(
                        slug=difficulty_slug
                    )
                except ObjectDoesNotExist:
                    raise KeyNotFoundError(
                        self.structure_file_path,
                        difficulty_slug,
                        "Difficulty Level"
                    )
            else:
                difficulty_level = None

            for question_type in question_types:
                slug = '{}-{}'.format(question_slug, question_type)
                question_class = VALID_QUESTION_TYPES[question_type]['question_class']
                defaults = dict()
                required_fields = ['title', 'question_text']

                if question_class == QuestionTypeParsons:
                    required_fields += ['lines']
                elif question_class == QuestionTypeDebugging:
                    required_fields += ['initial_code']
                    defaults['read_only_lines_top'] = int(question_data.get('number_of_read_only_lines_top', 0))
                    defaults['read_only_lines_bottom'] = int(question_data.get('number_of_read_only_lines_bottom', 0))
                
                #TODO remove conditional once all difficulty levels assigned
                if difficulty_level:
                    defaults['difficulty_level'] = difficulty_level

                question, created = question_class.objects.update_or_create(
                    slug=slug,
                    defaults=defaults,
                )

                self.populate_translations(question, question_translations)
                self.mark_translation_availability(question, required_fields=required_fields)
                question.save()

                # Add programming concepts
                concept_slugs = question_data.get("concepts", [])
                for concept_slug in concept_slugs:
                    try:
                        concept = ProgrammingConcepts.objects.get(
                            slug=concept_slug
                        )
                        if concept.children.exists():
                            raise InvalidYAMLValueError(
                                self.structure_file_path,
                                "concepts - value '{}' is invalid".format(concept_slug),
                                "Programming Concept with no children (parent concepts are not allowed)"
                            )
                        else:
                            question.concepts.add(concept)
                    except ObjectDoesNotExist:
                        raise KeyNotFoundError(
                            self.structure_file_path,
                            concept_slug,
                            "Concepts"
                        )

                # Add question contexts
                context_slugs = question_data.get("contexts", [])
                for context_slug in context_slugs:
                    try:
                        context = QuestionContexts.objects.get(
                            slug=context_slug
                        )
                        if context.children.exists():
                            raise InvalidYAMLValueError(
                                self.structure_file_path,
                                "contexts - value '{}' is invalid".format(context_slug),
                                "Question Context with no children (parent contexts are not allowed)"
                            )
                        else:
                            question.contexts.add(context)
                    except ObjectDoesNotExist:
                        raise KeyNotFoundError(
                            self.structure_file_path,
                            context_slug,
                            "Contexts"
                        )

                test_case_class = VALID_QUESTION_TYPES[question_type]['test_case_class']
                for (test_case_id, test_case_type) in question_test_cases.items():
                    test_case_translations = self.get_blank_translation_dictionary()

                    if question_class == QuestionTypeProgram:
                        test_case_input_filename = join(
                            question_slug,
                            TEST_CASE_FILE_TEMPLATE.format(id=test_case_id, type='input')
                        )
                        for language in get_available_languages():
                            test_case_input = open(self.get_localised_file(
                                language, test_case_input_filename), encoding='UTF-8').read()
                            test_case_translations[language]['test_input'] = test_case_input
                    elif question_class in (QuestionTypeFunction, QuestionTypeParsons, QuestionTypeDebugging):
                        test_case_code_filename = join(
                            question_slug,
                            TEST_CASE_FILE_TEMPLATE.format(id=test_case_id, type='code')
                        )
                        for language in get_available_languages():
                            test_case_code = open(self.get_localised_file(
                                language, test_case_code_filename), encoding='UTF-8').read()
                            test_case_translations[language]['test_code'] = test_case_code

                    test_case_output_filename = join(
                        question_slug,
                        TEST_CASE_FILE_TEMPLATE.format(id=test_case_id, type='output')
                    )
                    for language in get_available_languages():
                        test_case_output = open(self.get_localised_file(
                            language, test_case_output_filename), encoding='UTF-8').read()
                        test_case_translations[language]['expected_output'] = test_case_output

                    # Create test case
                    test_case, created = test_case_class.objects.update_or_create(
                        question=question,
                        number=test_case_id,
                        defaults={},
                    )

                    if test_case_class == QuestionTypeProgramTestCase:
                        required_fields = ['test_input', 'expected_output']
                    elif test_case_class in (
                        QuestionTypeFunctionTestCase,
                        QuestionTypeParsonsTestCase,
                        QuestionTypeDebuggingTestCase,
                    ):
                        required_fields = ['test_code', 'expected_output']

                    self.populate_translations(test_case, test_case_translations)
                    self.mark_translation_availability(test_case, required_fields=required_fields)
                    test_case.save()

                if created:
                    verb_text = 'Added'
                else:
                    verb_text = 'Updated'

                self.log('{} {} question: {}'.format(verb_text, question_type, question.title))
        self.log("All questions loaded!\n")


def clean_parsons_lines(code_lines):
    """Return list of lines of code, stripped of whitespace.

    Args:
        code (list): Code to be cleaned.

    Returns:
        List of cleaned code.
    """
    clean_lines = list()
    for line in code_lines:
        stripped_line = line.strip()
        if stripped_line:
            clean_lines.append(stripped_line)
    return clean_lines
