"""Views for programming application."""

import json
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.db.models import Count, Max, Exists, OuterRef
from django.db.models.functions import Coalesce
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
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
from programming.models import (
    Profile,
    Question,
    TestCase,
    Attempt,
    TestCaseAttempt,
    Like
)
from programming.codewof_utils import add_points, check_achievement_conditions
from programming.filters import QuestionFilter
from programming.utils import create_filter_helper

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
