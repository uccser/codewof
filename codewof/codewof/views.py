"""Views for codeWOF application."""

from django.views import generic
from django.http import JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
import json

from codewof.models import (
    Profile,
    Question,
    TestCase,
    Attempt,
    TestCaseAttempt,
)

QUESTION_JAVASCRIPT = 'js/question_types/{}.js'


class IndexView(generic.base.TemplateView):
    """Homepage for CodeWOF."""

    template_name = 'codewof/index.html'

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.select_subclasses()
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

    return JsonResponse(result)


class ProfileView(LoginRequiredMixin, generic.DetailView):
    """Displays a user's profile."""

    login_url = '/login/'
    redirect_field_name = 'next'
    template_name = 'codewof/profile.html'
    model = Profile

    def get_object(self):
        """Get object for template."""
        if self.request.user.is_authenticated:
            return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        return context


class QuestionListView(generic.ListView):
    """View for listing questions."""

    model = Question
    context_object_name = 'questions'

    def get_queryset(self):
        """Return questions objects for page.

        Returns:
            Question queryset.
        """
        return Question.objects.all().select_subclasses()


class QuestionView(generic.base.TemplateView):
    """Displays a question.

    This view requires to retrieve the object first in the context,
    in order to determine the required template to render.
    """

    template_name = 'codewof/question.html'

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)
        try:
            self.question = Question.objects.get_subclass(
                pk=self.kwargs['pk']
            )
        except Question.DoesNotExist:
            raise Http404("No question matches the given ID.")
        context['question'] = self.question
        test_cases = self.question.test_cases.values()
        context['test_cases'] = test_cases
        context['test_cases_json'] = json.dumps(list(test_cases))
        context['question_js'] = QUESTION_JAVASCRIPT.format(self.question.QUESTION_TYPE)

        if self.request.user.is_authenticated:
            try:
                previous_attempt = Attempt.objects.filter(
                    profile=self.request.user.profile,
                    question=self.question,
                ).latest('datetime')
            except ObjectDoesNotExist:
                previous_attempt = None
            context['previous_attempt'] = previous_attempt
        return context
