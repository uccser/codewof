import datetime
import json
import logging

from codewof.models import (
    Profile,
    Question,
    TestCase,
    Attempt,
    TestCaseAttempt,
    Badge,
    Earned,
)
from django.http import JsonResponse
from django.conf import settings

time_zone = settings.TIME_ZONE

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


def add_points(question, profile, attempt):
    """add appropriate number of points (if any) to user's account after a question is answered"""
    max_points_from_attempts = 3
    points_for_correct = 10

    num_attempts = len(Attempt.objects.filter(question=question, profile=profile))
    previous_corrects = Attempt.objects.filter(question=question, profile=profile, passed_tests=True)
    is_first_correct = len(previous_corrects) == 1

    points_to_add = 0

    # check if first passed
    if attempt.passed_tests and is_first_correct:
        # deduct one point for up to three failed attempts
        attempt_deductions = (num_attempts - 1) * 2
        points_to_add = points_for_correct - attempt_deductions
    else:
        # add up to three points immediately for attempts
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


def get_days_consecutively_answered(user):
    # get datetimes from attempts in date form)
    attempts = Attempt.objects.filter(profile=user.profile).datetimes('datetime', 'day', 'DESC')
    # get current day as date
    i = 0
    today = datetime.datetime.now().replace(tzinfo=None).date()

    while i < len(attempts):
        attempt = attempts[i]
        expected_date = today - datetime.timedelta(days=i)
        if attempt.date() != expected_date:
            break
        i += 1

    return i


def check_badge_conditions(user):
    """check badges for account creation, days logged in, and questions solved"""
    earned_badges = user.profile.earned_badges.all()
    # account creation badge
    try:
        creation_badge = Badge.objects.get(id_name="create-account")
        if creation_badge not in earned_badges:
            # create a new account creation
            new_achievement = Earned(profile=user.profile, badge=creation_badge)
            new_achievement.full_clean()
            new_achievement.save()
    except Badge.DoesNotExist:
        logger.warning("No such badge: create-account")
        pass

    # check questions solved badges
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

    # checked questions attempted badges
    try:
        attempt_badges = Badge.objects.filter(id_name__contains="attempts-made")
        attempted = Attempt.objects.filter(profile=user.profile)
        for attempt_badge in attempt_badges:
            if attempt_badge not in earned_badges:
                num_questions = int(attempt_badge.id_name.split("-")[2])
                if len(attempted) >= num_questions:
                    new_achievement = Earned(profile=user.profile, badge=attempt_badge)
                    new_achievement.full_clean()
                    new_achievement.save()
    except Badge.DoesNotExist:
        logger.warning("No such badges: attempts-made")
        pass

    # consecutive days logged in badges

    num_consec_days = -1
    consec_badges = Badge.objects.filter(id_name__contains="consecutive-days")
    for consec_badge in consec_badges:
        if consec_badge not in earned_badges:
            if num_consec_days == -1:
                num_consec_days = get_days_consecutively_answered(user)
            n_days = int(consec_badge.id_name.split("-")[2])
            if n_days == num_consec_days:
                logger.warning("make new consec badge")
                new_achievement = Earned(profile=user.profile, badge=consec_badge)
                new_achievement.full_clean()
                new_achievement.save()

            # days_logged_in = LoginDay.objects.filter(profile=user.profile)
            # days_logged_in = sorted(days_logged_in, key=lambda k: k.day, reverse=True)
            # sections = get_consecutive_sections([d.day for d in days_logged_in])

            # max_consecutive = len(max(sections, key=lambda k: len(k)))
            #
            # if max_consecutive >= n_days:
            #     new_achievement = Earned(profile=user.profile, badge=login_badge)
            #     new_achievement.full_clean()
            #     new_achievement.save()


def get_past_5_weeks(user):
    """get how many questions a user has done each week for the last 5 weeks"""
    # t = datetime.date.today()
    # today = datetime.datetime(t.year, t.month, t.day)
    # last_monday = today - datetime.timedelta(days=today.weekday(), weeks=0)
    # last_last_monday = today - datetime.timedelta(days=today.weekday(), weeks=1)

    past_5_weeks = []
    # to_date = today
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
