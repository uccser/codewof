"""Views for codeWOF application."""
import datetime

from django.views import generic
from django.http import JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
import json
import logging

from codewof.models import (
    Profile,
    Question,
    TestCase,
    Attempt,
    TestCaseAttempt,
    Badge,
    Earned
)

logger = logging.getLogger(__name__)
del logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'incremental': True,
    'root': {
        'level': 'DEBUG',
    },
}


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

            add_points(question, profile, attempt)

            result['success'] = True

    return JsonResponse(result)


def add_points(question, profile, attempt):
    """add appropriate number of points (if any) to user's account"""
    max_points_from_attempts = 3
    points_for_correct = 10

    num_attempts = len(Attempt.objects.filter(question=question, profile=profile))
    previous_corrects = Attempt.objects.filter(question=question, profile=profile, passed_tests=True)
    is_first_correct = len(previous_corrects) == 1

    points_to_add = 0

    if attempt.passed_tests and is_first_correct:
        attempt_deductions = 0 if num_attempts == 1 else num_attempts * 2 if num_attempts < max_points_from_attempts \
            else max_points_from_attempts * 2
        points_to_add = points_for_correct - attempt_deductions
    else:
        if num_attempts <= max_points_from_attempts:
            points_to_add += 1

    profile.points += points_to_add
    profile.full_clean()
    profile.save()


def save_goal_choice(request):
    """update user's goal choice in database"""
    request_json = json.loads(request.body.decode('utf-8'))
    if request.user.is_authenticated:
        user = request.user
        profile = user.profile

        goal_choice = request_json['goal_choice']
        profile.goal = int(goal_choice)
        profile.full_clean()
        profile.save()

    return JsonResponse({})


def get_consecutive_sections(days_logged_in):
    """return a list of lists of consecutive days logged in"""
    consecutive_sections = []

    today = days_logged_in[0]
    previous_section = [today]
    for day in days_logged_in[1:]:
        if day == previous_section[-1] - datetime.timedelta(days=1):
            previous_section.append(day)
        else:
            consecutive_sections.append(previous_section)
            previous_section = [day]

    consecutive_sections.append(previous_section)
    return consecutive_sections


def check_badge_conditions(user):
    """check badges for account creation, days logged in, and questions solved"""
    earned_badges = user.profile.earned_badges.all()

    # account creation badge
    try:
        creation_badge = Badge.objects.get(id_name="create-account")
        if creation_badge not in earned_badges:
            new_achievement = Earned(profile=user.profile, badge=creation_badge)
            new_achievement.full_clean()
            new_achievement.save()
    except Badge.DoesNotExist:
        logger.warning("No such badge: create-account")
        pass

    try:
        question_badges = Badge.objects.filter(id_name__contains="questions-solved")
        solved = Attempt.objects.filter(profile=user.profile, passed_tests=True)
        for question_badge in question_badges:
            if question_badge not in earned_badges:
                num_questions = int(question_badge.id_name.split("-")[2])
                if len(solved) >= num_questions:
                    new_achievement = Earned(profile=user.profile, badge=question_badge)
                    new_achievement.full_clean()
                    new_achievement.save()
    except Badge.DoesNotExist:
        logger.warning("No such badges: questions-solved")
        pass

    try:
        attempt_badges = Badge.objects.filter(id_name__contains="attempts-made")
        attempted = Attempt.objects.filter(profile=user.profile)
        for attempt_badge in attempt_badges:
            if attempt_badge not in earned_badges:
                num_questions = int(attempt_badge.id_name.split("-")[2])
                logger.warning(attempt_badge.id_name)
                logger.warning(num_questions)
                logger.warning(len(attempted))
                if len(attempted) >= num_questions:
                    logger.warning("making badge")
                    new_achievement = Earned(profile=user.profile, badge=attempt_badge)
                    new_achievement.full_clean()
                    new_achievement.save()
    except Badge.DoesNotExist:
        logger.warning("No such badges: questions-solved")
        pass


    # consecutive days logged in badges
    # login_badges = Badge.objects.filter(id_name__contains="login")
    # for login_badge in login_badges:
    #     if login_badge not in earned_badges:
    #         n_days = int(login_badge.id_name.split("-")[1])
    #
    #         days_logged_in = LoginDay.objects.filter(profile=user.profile)
    #         days_logged_in = sorted(days_logged_in, key=lambda k: k.day, reverse=True)
    #         sections = get_consecutive_sections([d.day for d in days_logged_in])
    #
    #         max_consecutive = len(max(sections, key=lambda k: len(k)))
    #
    #         if max_consecutive >= n_days:
    #             new_achievement = Earned(profile=user.profile, badge=login_badge)
    #             new_achievement.full_clean()
    #             new_achievement.save()


def get_past_5_weeks(user):
    """get how many questions a user has done each week for the last 5 weeks"""
    t = datetime.date.today()
    today = datetime.datetime(t.year, t.month, t.day)
    last_monday = today - datetime.timedelta(days=today.weekday(), weeks=0)
    last_last_monday = today - datetime.timedelta(days=today.weekday(), weeks=1)

    past_5_weeks = []
    to_date = today
    # for week in range(0, 5):
    #     from_date = today - datetime.timedelta(days=today.weekday(), weeks=week)
    #     attempts = Attempt.objects.filter(profile=user.profile, date__range=(from_date, to_date + datetime.timedelta(days=1)), is_save=False)
    #     distinct_questions_attempted = attempts.values("question__pk").distinct().count()-
    #
    #     label = str(week) + " weeks ago"
    #     if week == 0:
    #         label = "This week"
    #     elif week == 1:
    #         label = "Last week"
    #
    #     past_5_weeks.append({'week': from_date, 'n_attempts': distinct_questions_attempted, 'label': label})
    #     to_date = from_date
    return past_5_weeks


class ProfileView(LoginRequiredMixin, generic.DetailView):
    """Displays a user's profile."""

    login_url = '/login/'
    redirect_field_name = 'next'
    template_name = 'codewof/profile.html'
    model = Profile

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        context = super().get_context_data(**kwargs)

        user = self.request.user

        check_badge_conditions(user)

        context['goal'] = user.profile.goal
        context['all_badges'] = Badge.objects.all()
        logger.warning(len(Badge.objects.all()))
        context['past_5_weeks'] = get_past_5_weeks(user)
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
        questions = Question.objects.all().select_subclasses()
        if self.request.user.is_authenticated:
            # TODO: Check if passeed in last 90 days
            for question in questions:
                question.completed = Attempt.objects.filter(
                    profile=self.request.user.profile,
                    question=question,
                    passed_tests=True,
                ).exists()
        return questions


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
