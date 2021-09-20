"""Custom loader for loading difficulty levels."""

from django.db import transaction
from utils.TranslatableModelLoader import TranslatableModelLoader
from utils.errors import MissingRequiredFieldError
from programming.models import DifficultyLevel

TEST_CASE_FILE_TEMPLATE = 'test-case-{id}-{type}.txt'


class DifficultiesLoader(TranslatableModelLoader):
    """Custom loader for loading difficulties."""

    @transaction.atomic
    def load(self):
        """Load questions.

        Raise:
            MissingRequiredFieldError: when no object can be found with the matching
                attribute.
        """
        difficulties_structure = self.load_yaml_file(self.structure_file_path)

        difficulty_translations = self.get_blank_translation_dictionary()
        required_translation_fields = ["name"]
        difficulties_translations = self.get_yaml_translations(
            self.structure_filename,
            required_fields=required_translation_fields,
            required_slugs=difficulties_structure.keys()
        )

        for (difficulty_slug, difficulty_data) in difficulties_structure.items():
            # Check test cases exist
            try:
                difficulty_level = difficulty_data['level']
            except KeyError:
                raise MissingRequiredFieldError(
                    self.structure_file_path,
                    [
                        'level',
                    ],
                    'Difficulty'
                )
            difficulty_translations = difficulties_translations.get(difficulty_slug, dict())

            defaults = dict()
            defaults["level"] = difficulty_level

            difficulty, created = DifficultyLevel.objects.update_or_create(
                slug=difficulty_slug,
                defaults=defaults,
            )

            self.populate_translations(difficulty, difficulty_translations)
            self.mark_translation_availability(difficulty, required_fields=required_translation_fields)
            difficulty.save()

            if created:
                verb_text = 'Added'
            else:
                verb_text = 'Updated'

            self.log(f'{verb_text} difficulty: {difficulty.name}')
        self.log("All difficulties loaded!\n")
