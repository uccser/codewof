"""Views for programming application."""

import json
import yaml
import os
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse
from django.db.models import Count, Max, Exists, OuterRef
from django.db.models.functions import Coalesce
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.shortcuts import redirect
from django_filters.views import FilterView
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from programming.question_recommendations import get_recommended_questions, get_recommendation_descriptions
from programming.serializers import (
    QuestionSerializer,
    ProfileSerializer,
    AttemptSerializer,
    LikeSerializer
)
import programming.models
from programming.models import (
    Profile,
    Question,
    Draft,
    DraftTestCase,
    DraftMacro,
    DraftMacroValue,
    TestCase,
    Attempt,
    TestCaseAttempt,
    Like,
    ProgrammingConcepts,
    QuestionContexts,
)
from programming.codewof_utils import add_points, check_achievement_conditions
from programming.filters import QuestionFilter, DraftFilter
from programming.utils import create_filter_helper
from programming.forms import NewQuestionForm, MacroForm, TestCaseForm

QUESTION_JAVASCRIPT = 'js/question_types/{}.js'


class QuestionListView(LoginRequiredMixin, FilterView):
    """View for listing questions."""

    filterset_class = QuestionFilter
    context_object_name = 'questions'
    template_name = 'programming/question_list.html'

    def get_queryset(self):
        """Return questions objects for page.

        Returns:
            Question queryset.
        """
        user_successful_attempt_subquery = Attempt.objects.filter(
            profile=self.request.user.profile,
            question=OuterRef('pk'),
            passed_tests=True,
        )
        questions = (
            Question.objects.all()
            .select_subclasses()
            .select_related('difficulty_level')
            .prefetch_related(
                'concepts',
                'concepts__parent',
                'contexts',
                'contexts__parent',
            )
            .order_by('difficulty_level')
            .annotate(completed=Exists(user_successful_attempt_subquery))
        )
        return questions

    def get_context_data(self, **kwargs):
        """Provide the context data for the question list view.

        Returns: Dictionary of context data.
        """
        user = self.request.user

        context = super().get_context_data(**kwargs)
        context['filter_formatter'] = create_filter_helper("programming:question_list")
        recommendation_descriptions = get_recommendation_descriptions()
        recommended_questions = get_recommended_questions(user.profile)
        if len(recommendation_descriptions) == len(recommended_questions):
            context['recommendations'] = [(description, question) for description, question in zip(
                recommendation_descriptions, recommended_questions
            )]
        context['filter_button_pressed'] = "submit" in self.request.GET
        return context


class DraftQuestionListView(LoginRequiredMixin, FilterView):
    """View for listing draft questions created by the user."""

    filterset_class = DraftFilter
    model = Draft
    context_object_name = 'drafts'
    template_name = 'programming/draft_list.html'

    def get_queryset(self):
        """Return draft questions objects for page.

        Returns:
            Draft question queryset.
        """
        drafts = (
            Draft.objects.filter(author_id=self.request.user.profile)
            .select_related('difficulty_level')
            .prefetch_related(
                'concepts',
                'concepts__parent',
                'contexts',
                'contexts__parent',
            )
            .order_by('difficulty_level')
        )
        return drafts

    def get_context_data(self, **kwargs):
        """Provide the context data for the question list view.

        Returns: Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['filter_formatter'] = create_filter_helper("programming:draft_list")
        context['filter_button_pressed'] = "submit" in self.request.GET
        return context


class DeleteQuestionView(LoginRequiredMixin, generic.base.TemplateView):
    """A "view" to handle requests to delete drafts."""

    model = Draft

    def get_object(self, **kwargs):
        """Get draft object."""
        try:
            draft = Draft.objects.get_subclass(
                pk=self.kwargs['pk']
            )
        except Draft.DoesNotExist:
            raise Http404("No draft question matches the given ID.")

        return draft

    def post(self, request, *args, **kwargs):
        """Check that the user is the author of the draft, and if so delete it."""
        self.object = self.get_object()
        if not request.user.is_authenticated or not request.user == self.object.author.user:
            return HttpResponseForbidden()
        self.object.delete()
        messages.info(request, 'Question deleted successfully.')
        return redirect(reverse('programming:draft_list'))


class SubmitQuestionView(LoginRequiredMixin, generic.CreateView):
    """Handles request to create a new question from a draft."""

    template_name = 'programming/add_question.html'
    model = Draft

    def get_object(self, **kwargs):
        """Get draft object for submission."""
        try:
            draft = Draft.objects.get_subclass(
                pk=self.kwargs['pk']
            )
        except Draft.DoesNotExist:
            raise Http404("No draft question matches the given ID.")

        return draft

    def create_question_from_draft(self):
        """Create a question model based on draft without saving it."""
        # Choose question model appropriately for the type
        model_name = f"QuestionType{self.object.question_type.title()}"
        class_ = getattr(programming.models, model_name)
        question = class_()

        # Populate model with appropriate information
        # Default fields
        question.slug = self.object.slug
        question.languages = self.object.languages
        question.title = self.object.title
        question.question_type = self.object.question_type
        question.question_text = self.object.question_text
        question.solution = self.object.solution
        question.difficulty_level = self.object.difficulty_level

        # Model-specific fields
        if self.object.question_type == 'parsons':
            # Parsons
            question.lines = self.object.lines

        elif self.object.question_type == 'debugging':
            # Debugging
            question.initial_code = self.object.initial_code
            question.read_only_lines_top = self.object.read_only_lines_top
            question.read_only_lines_bottom = self.object.read_only_lines_bottom

        return question

    def is_valid_question(self, request):
        """
        Check whether the question created is valid.

        Creates a question from the draft in self.object, adds messages for
        any problems to the request, and returns a boolean describing whether
        the question is valid.
        """
        valid = True
        # Create (do NOT save) a question model based on draft
        question = self.create_question_from_draft()

        # Verify there is at least one concept and one test case
        if len(self.object.concepts.values()) == 0:
            messages.error(request, 'Questions must have at least one concept')
            valid = False

        if len(self.object.draft_test_cases.values()) == 0:
            messages.error(request, 'Questions must have at least one test case')

        # Check the question model
        try:
            question.full_clean()
        except ValidationError as e:
            error_map = {
                'title': 'Questions must have a title',
                'type': 'Questions must have a type',
                'difficulty': 'Questions must have a difficulty',
                'question_text': 'Question text cannot be empty',
                'solution': 'Solution cannot be empty',
            }
            for msg in e.message_dict:
                messages.error(request, error_map[msg])
            return False

        # Make new folder (a uniqueness check of the slug)
        try:
            os.mkdir(f'./programming/review/en/{self.object.slug}')
        except FileExistsError:
            messages.error(request, 'A question with that title already exists')
            return False
        except Exception:
            messages.error(request, 'An unexpected error occurred')
            return False

        # Return boolean of whether it is valid
        return valid

    def generate_yaml(self):
        """
        Generate the YAML to go in questions.yaml.

        Generates yaml with the following format:
        title:
          types:
            -
          [number_of_read_only_lines_top: <n>]
          [number_of_read_only_lines_bottom: <n>]
          [parsons-extra-lines:
            - ]
          test-cases:
            1: <normal|exceptional>
          difficulty: difficulty-<1|2|3|4>
          concepts:
            -
          [contexts:
            - ]
        """
        # Preparation of different question types
        before_test_cases = [
            {'type': [self.object.question_type]},
        ]

        if self.object.question_type == 'parsons':
            before_test_cases[0]['types'] = ['function', 'parsons']
            del before_test_cases[0]['type']
            if self.object.lines is not None:
                before_test_cases.append({'parsons-extra-lines': [self.object.extra_lines]})
        elif self.object.question_type == 'debugging':
            before_test_cases += [
                {'number_of_read_only_lines_top': self.object.number_of_read_only_lines_top},
                {'number_of_read_only_lines_bottom': self.object.number_of_read_only_lines_bottom},
            ]

        # Test cases
        test_cases = []
        for test_case in list(self.object.draft_test_cases.values()):
            test_cases.append({test_case['number']: test_case['type']})
        test_cases = [{'test-cases': sorted(test_cases, key=lambda x: x.keys())}]

        # Difficulty, concepts, and contexts
        after_test_cases = [
            {'difficulty': self.object.difficulty_level.slug},
            {'concepts': [concept['slug'] for concept in list(self.object.concepts.values())]},
        ]
        contexts = list(self.object.contexts.values())
        if len(contexts) > 0:
            after_test_cases.append({'contexts': [context['slug'] for context in contexts]})

        # Join together
        return [{self.object.title: before_test_cases + test_cases + after_test_cases}]

    def generate_markdown(self):
        """Create markdown for question.md file."""
        lines = [f"# {self.object.title}"]

        for line in self.object.question_text.split('<p>'):
            lines.append(line.replace('</p>', '\n')
                             .replace('<strong>', '**')
                             .replace('</strong>', '**')
                             .replace('<code>', '`')
                             .replace('</code>', '`'))

        return '\n'.join(lines)

    def generate_files(self):
        """Generate all the stored files for a question."""
        # YAML for structure file
        with open(f'./programming/review/structure/{self.object.slug}.yaml', 'w') as file:
            yaml.dump(self.generate_YAML(), file)

        # Question text
        with open(f'./programming/review/en/{self.object.slug}/question.md', 'w') as file:
            file.write(self.generate_markdown())

        # Question solution
        with open(f'./programming/review/en/{self.object.slug}/solution.py', 'w') as file:
            # Add a newline to the end of the file if needed
            solution = self.object.solution
            solution_lines = self.object.solution.split('/n')
            if solution_lines[-1] != '':
                solution += '\n'

            file.write(solution)

        # Initial code (for debugging)
        if self.object.question_type == 'debugging':
            with open(f'./programming/review/en/{self.object.slug}/initial.py', 'w') as file:
                file.write(self.object.initial_code)

        # Iterate through test cases
        test_case_suffix = 'input' if self.object.question_type == 'program' else 'code'
        for test_case in list(self.object.draft_test_cases.values()):
            test_case_file_prefix = f'./programming/review/en/{self.object.slug}/test-case-{test_case["number"]}'
            with open(f'{test_case_file_prefix}-{test_case_suffix}.txt', 'w') as file:
                file.write(test_case["test_code"])
            with open(f'{test_case_file_prefix}-output.txt', 'w') as file:
                file.write(test_case["expected_output"])

        # Create YAML file to store the macros
        macros = []
        for macro in DraftMacro.objects.filter(draft=self.object):
            values = []
            for value in list(macro.macro_values.values()):
                values.append(value['value'])
            macros.append({macro.placeholder: values})
        if len(macros) > 0:
            with open(f'./programming/review/en/{self.object.slug}/macros.yaml', 'w') as file:
                yaml.dump(macros, file)

    def post(self, request, *args, **kwargs):
        """Handle post request to submit a draft."""
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()

        if self.is_valid_question(request):
            # Generate files
            self.generate_files()

            # Delete from database
            self.object.delete()

            # Send user to question list page
            messages.info(request, 'Question submitted successfully.')
            return redirect(reverse('programming:draft_list'))

        # Question was invalid, send user to question creation form to fix the issues
        return redirect(reverse('programming:edit_draft', kwargs={'pk': self.kwargs['pk']}))


class DraftQuestionView(LoginRequiredMixin, generic.CreateView, generic.UpdateView):
    """Display the form for editing a draft question."""

    template_name = 'programming/add_question.html'
    template_name_suffix = ''
    form_class = NewQuestionForm
    model = Draft

    def get_object(self, **kwargs):
        """Get question object for view."""
        try:
            if 'pk' in self.kwargs:
                draft = Draft.objects.get_subclass(
                    pk=self.kwargs['pk']
                )
            else:
                # Here, we create a new question
                draft = None
        except Draft.DoesNotExist:
            raise Http404("No draft question matches the given ID.")

        return draft

    def get_context_data(self, **kwargs):
        """
        Provide the context data for the create/edit question view.

        Returns: Dictionary of context data.
        """
        context = super().get_context_data(**kwargs)
        context['question'] = self.object
        if context['question'] is not None:
            test_cases = self.object.draft_test_cases.values()
            context['test_cases'] = test_cases
            context['test_cases_json'] = json.dumps(list(test_cases))

            fetched_macros = DraftMacro.objects.filter(draft=self.object)
            macros = []
            for macro in fetched_macros:
                macro_values = macro.macro_values.values()
                macros.append({
                    'placeholder': macro.placeholder,
                    'values': [macro_val['value'] for macro_val in macro_values]
                })

            context['macros_json'] = json.dumps(list(macros))
        context['forms'] = {
            "main_form": NewQuestionForm(instance=context['question']),
            "macro_form": MacroForm(),
            "test_case_form": TestCaseForm(),
        }

        return context

    def _custom_split(self, string):
        """Split on commas, but allow backslashes to escape splitting."""
        parts = string.split(',')
        i = 1
        output = [parts[0]]

        while i < len(parts):
            if output[-1].endswith('\\'):
                output[-1] = output[-1][:-1] + ',' + parts[i]
            else:
                output.append(parts[i])
            i += 1

        return output

    def form_valid(self, form, *args, **kwargs):
        """Save the draft when a valid form is submitted."""
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()

        # First save the draft
        draft = form.save(commit=False)
        if self.object is None:
            # New draft
            draft.languages = ['en']
            draft.author_id = self.request.user.id
        draft.slug = self._generate_slug(form.cleaned_data)
        draft.save()

        # Then fetch/save many-to-many fields
        # Concepts
        concept_names = form.cleaned_data.get('concepts')
        if 'conditionals' in concept_names:
            concept_names.remove('conditionals')
            concept_names += [form.cleaned_data.get('concept_conditionals')]
        if 'loops' in concept_names:
            concept_names.remove('loops')
            concept_names += [form.cleaned_data.get('concept_loops')]

        # Contexts
        context_names = form.cleaned_data.get('contexts')
        if 'mathematics' in context_names:
            context_names.remove('mathematics')
            context_names += [form.cleaned_data.get('context_mathematics')]
            context_names.remove('')    # Handle the case where only geometry is selected
        if form.cleaned_data.get('context_has_geometry'):
            context_names += [form.cleaned_data.get('context_geometry')]

        # Test cases
        test_case_lines = form.cleaned_data.get('test_cases').split('\n')
        saved_test_cases = DraftTestCase.objects.filter(draft=draft)
        for i in range(len(test_case_lines)):
            parts = test_case_lines[i].split('@@')
            if len(parts) != 3:
                continue
            given_type = parts[0]
            code = parts[1]
            expected_output = parts[2]

            if i < len(saved_test_cases):
                test_case = saved_test_cases[i]
            else:
                test_case = DraftTestCase()

            # Fill data
            test_case.number = i + 1
            test_case.type = given_type
            test_case.test_code = code
            test_case.expected_output = expected_output
            test_case.draft = draft

            test_case.save()
        # Remove test cases that have been deleted
        for j in range(i + 1, len(saved_test_cases)):
            saved_test_cases[j].delete()

        # Macros
        macro_lines = form.cleaned_data.get('macros').split('\n')
        saved_macros = DraftMacro.objects.filter(draft=draft)
        for i in range(len(macro_lines)):
            parts = macro_lines[i].split('@@')
            if len(parts) != 2:
                continue
            name = parts[0]
            values = self._custom_split(parts[1])

            if i < len(saved_macros):
                macro = saved_macros[i]
            else:
                macro = DraftMacro()

            macro.placeholder = name
            macro.draft = draft
            macro.save()

            saved_values = DraftMacroValue.objects.filter(macro=macro)
            for j in range(len(values)):
                if j < len(saved_values):
                    possible_value = saved_values[j]
                else:
                    possible_value = DraftMacroValue()
                possible_value.macro = macro
                possible_value.value = values[j]
                possible_value.save()

            # Remove values that have been deleted
            for k in range(j + 1, len(saved_values)):
                # saved_values[k].delete()
                print("Delete value")
        # Remove macros that have been deleted
        for j in range(i + 1, len(saved_macros)):
            # saved_macros[j].delete()
            print("Delete macro")

        # Apply many-to-many fields to question
        for name in concept_names:
            concept_obj = ProgrammingConcepts.objects.get(slug=name)
            draft.concepts.add(concept_obj)

        for name in context_names:
            context_obj = QuestionContexts.objects.get(slug=name)
            draft.contexts.add(context_obj)

        return redirect(self.get_success_url())

    def _generate_slug(self, cleaned):
        """
        Create a slug for new questions in a similar style to existing questions.

        Make title lowercase, replace spaces with hyphens, and add -<question type> to the end.
        """
        return f"{cleaned['title'].lower().replace(' ', '-')}-{cleaned['question_type']}"

    def form_invalid(self, form):
        """Take action if form is invalid."""
        return super().form_invalid(form)

    def get_success_url(self):
        """Define the url to visit on a success."""
        return reverse('programming:draft_list')


class QuestionView(LoginRequiredMixin, generic.DetailView):
    """Displays a question.

    This view requires to retrieve the object first in the context,
    in order to determine the required template to render.
    """

    template_name = 'programming/question.html'

    def get_object(self, **kwargs):
        """Get question object for view."""
        try:
            question = Question.objects.get_subclass(
                pk=self.kwargs['pk']
            )
        except Question.DoesNotExist:
            raise Http404("No question matches the given ID.")

        return question

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        context['question'] = self.object
        test_cases = self.object.test_cases.values()
        context['test_cases'] = test_cases
        context['test_cases_json'] = json.dumps(list(test_cases))
        context['question_js'] = QUESTION_JAVASCRIPT.format(self.object.QUESTION_TYPE)

        if self.request.user.is_authenticated:
            try:
                previous_attempt = Attempt.objects.filter(
                    profile=self.request.user.profile,
                    question=self.object,
                ).latest('datetime')
            except ObjectDoesNotExist:
                previous_attempt = None
            context['previous_attempt'] = previous_attempt
        return context


def save_question_attempt(request):
    """Save user's attempt for a question.

    If the attempt is successful: add points if these haven't already
    been added.

    Args:
        request (Request): AJAX request from user.

    Returns:
        JSON response with result.
    """
    result = {
        'success': False,
    }
    if request.is_ajax():
        if request.user.is_authenticated:
            request_json = json.loads(request.body.decode('utf-8'))
            profile = request.user.profile
            question = Question.objects.get(pk=request_json['question'])
            user_code = request_json['user_input']

            # If same as previous attempt, don't save to database
            previous_attempt = Attempt.objects.filter(
                profile=profile,
                question=question,
            ).order_by('-datetime').first()
            if not previous_attempt or user_code != previous_attempt.user_code:
                test_cases = request_json['test_cases']
                total_tests = len(test_cases)
                total_passed = 0
                for test_case in test_cases.values():
                    if test_case['passed']:
                        total_passed += 1

                attempt = Attempt.objects.create(
                    profile=profile,
                    question=question,
                    user_code=user_code,
                    passed_tests=total_passed == total_tests,
                )

                # Create test case attempt objects
                for test_case_id, test_case_data in test_cases.items():
                    test_case = TestCase.objects.get(pk=test_case_id)
                    TestCaseAttempt.objects.create(
                        attempt=attempt,
                        test_case=test_case,
                        passed=test_case_data['passed'],
                    )
                result['success'] = True
                points_before = profile.points
                points = add_points(question, profile, attempt)
                achievements = check_achievement_conditions(profile)
                points_after = profile.points
                result['curr_points'] = points
                result['point_diff'] = points_after - points_before
                result['achievements'] = achievements
            else:
                result['success'] = False
                result['message'] = 'Attempt not saved, same as previous attempt.'

    return JsonResponse(result)


class CreateView(generic.base.TemplateView):
    """Page for creation programming questions."""

    template_name = 'programming/create.html'

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        question_types = list()
        for question_type_class in Question.__subclasses__():
            data = dict()
            data['name'] = question_type_class.QUESTION_TYPE.capitalize()
            data['count'] = question_type_class.objects.count()
            max_answered = Profile.objects.filter(
                attempt__question__in=question_type_class.objects.all(),
                attempt__passed_tests=True,
            ).annotate(
                max_answered_by_user=Count('attempt__question', distinct=True)
            ).aggregate(
                max_answered=Coalesce(Max('max_answered_by_user'), 0)
            )
            data['unanswered_count'] = data['count'] - max_answered['max_answered']
            question_types.append(data)
        context['question_types'] = question_types
        return context


class QuestionAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows questions to be viewed."""

    queryset = Question.objects.all().prefetch_related('attempt_set')
    serializer_class = QuestionSerializer


class ProfileAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows profiles to be viewed.

    There is currently no URL set up to access this.
    Helper for AttemptAPIViewSet.
    """

    permission_classes = [IsAdminUser]
    queryset = Profile.objects.all().prefetch_related('user')
    serializer_class = ProfileSerializer


class AttemptAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows attempts to be viewed."""

    permission_classes = [IsAdminUser]
    queryset = Attempt.objects.all().prefetch_related('profile')
    serializer_class = AttemptSerializer


@require_http_methods(["POST"])
@login_required()
def like_attempt(request, pk):
    """View for liking an attempt."""
    user = request.user
    attempt = Attempt.objects.get(pk=pk)

    if user == attempt.profile.user:
        raise Exception("User cannot like their own attempt.")
    if Like.objects.filter(user=user, attempt=attempt).exists():
        raise Exception("Cannot like an attempt more than once.")

    Like(user=user, attempt=attempt).save()
    return HttpResponse()


@require_http_methods(["DELETE"])
@login_required()
def unlike_attempt(request, pk):
    """View for unliking an attempt."""
    user = request.user
    attempt = Attempt.objects.get(pk=pk)

    like = Like.objects.filter(user=user, attempt=attempt)
    if not like.exists():
        raise Exception("Can only unlike liked attempts.")

    like.delete()
    return HttpResponse()


class LikeAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows attempt likes to be viewed."""

    permission_classes = [IsAdminUser]
    queryset = Like.objects.all().select_related('user', 'attempt')
    serializer_class = LikeSerializer
