import datetime
import json
import logging

from programming.models import (
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
    num_attempts = Attempt.objects.filter(question=question, profile=profile)
    is_first_correct = len(Attempt.objects.filter(question=question, profile=profile, passed_tests=True)) == 1
    logger.warning(num_attempts)
    logger.warning(is_first_correct)
    points_to_add = 0

    # check if first passed
    if attempt.passed_tests and is_first_correct:
        points_to_add += 10
        if len(num_attempts) == 1:
            # correct first try
            points_to_add += 1

    profile.points += points_to_add
    profile.full_clean()
    profile.save()
    return profile.points


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


def get_days_consecutively_answered(user):
    """Gets the number of consecutive days with questions attempted"""
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


def get_days_with_solutions(user):
    """Gets a list of dates with questions successfully answered."""
    today = datetime.datetime.now().replace(tzinfo=None).date()
    attempts = Attempt.objects.filter(profile=user.profile, datetime__year=today.year, passed_tests=True).datetimes(
        'datetime', 'day', 'DESC')
    return attempts


def check_badge_conditions(user):
    """check badges for account creation, consecutive days with questions answered, attempts made, points earned,
     and questions solved"""
    earned_badges = user.profile.earned_badges.all()
    new_badges = []
    # account creation badge
    try:
        creation_badge = Badge.objects.get(id_name="create-account")
        if creation_badge not in earned_badges:
            # create a new account creation
            new_achievement = Earned(profile=user.profile, badge=creation_badge)
            new_achievement.full_clean()
            new_achievement.save()
            new_badges.append(new_achievement)
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
                    new_badges.append(new_achievement)
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
                    new_badges.append(new_achievement)
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
                new_achievement = Earned(profile=user.profile, badge=consec_badge)
                new_achievement.full_clean()
                new_achievement.save()
                new_badges.append(new_achievement)
    # user.profile = backdate_points(user.profile)
    # backdate_badges(user.profile)
    return new_badges


def backdate_points_and_badges():
    """Performs backdate of all points and badges for each profile in the system."""
    profiles = Profile.objects.all()
    for profile in profiles:
        profile = backdate_badges(profile)
        profile = backdate_points(profile)
        # save profile when update is completed
        profile.full_clean()
        profile.save()


def backdate_points(profile):
    """Re-calculates points for the user profile."""
    questions = Question.objects.all()
    profile.points = 0
    for question in questions:
        has_passed = len(Attempt.objects.filter(profile=profile, question=question, passed_tests=True)) > 0
        user_attempts = Attempt.objects.filter(profile=profile, question=question)
        first_passed = False
        if len(user_attempts) > 0:
            first_passed = user_attempts[0].passed_tests
        if has_passed:
            profile.points += 10
        if first_passed:
            profile.points += 1
    return profile


def backdate_badges(profile):
    """Re-checks the profile for badges earned."""
    check_badge_conditions(profile.user)
    return profile
