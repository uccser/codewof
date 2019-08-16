"""Views for programming application."""

from django.views import generic
from django.utils import timezone
from django.http import JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
import json
from programming.models import (
    Question,
    TestCase,
    Attempt,
    TestCaseAttempt,
)
from research.models import StudyRegistration

QUESTION_JAVASCRIPT = 'js/question_types/{}.js'


class IndexView(generic.base.TemplateView):
    """Homepage for programming."""

    template_name = 'programming/index.html'

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.select_subclasses()
        return context


class QuestionListView(LoginRequiredMixin, generic.ListView):
    """View for listing questions."""

    model = Question
    context_object_name = 'questions'

    def get_queryset(self):
        """Return questions objects for page.

        Returns:
            Question queryset.
        """
        now = timezone.now()
        if self.request.user.is_authenticated:
            # Look for active study registration
            try:
                study_registration = StudyRegistration.objects.get(
                    user=self.request.user,
                    study_group__study__start_date__lte=now,
                    study_group__study__end_date__gte=now,
                )
            except ObjectDoesNotExist:
                study_registration = None

        if study_registration:
            questions = study_registration.study_group.questions.select_subclasses()
        else:
            questions = Question.objects.all().select_subclasses()

        if self.request.user.is_authenticated:
            # TODO: Check if passed in last 90 days
            for question in questions:
                question.completed = Attempt.objects.filter(
                    profile=self.request.user.profile,
                    question=question,
                    passed_tests=True,
                ).exists()
        return questions


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

        if self.request.user.is_authenticated:
            # Look for active study registration
            now = timezone.now()
            try:
                study_registration = StudyRegistration.objects.get(
                    user=self.request.user,
                    study_group__study__start_date__lte=now,
                    study_group__study__end_date__gte=now,
                )
            except StudyRegistration.DoesNotExist:
                study_registration = None
            if study_registration and question not in study_registration.study_group.questions.select_subclasses():
                raise PermissionDenied
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
            else:
                result['success'] = False
                result['message'] = 'Attempt not saved, same as previous attempt.'

    return JsonResponse(result)
