"""Utility functions for codeWOF system. Involves points, badges, and backdating points and badges per user."""

import datetime
import json
import logging
from dateutil.relativedelta import relativedelta

from programming.models import (
    Profile,
    Question,
    Attempt,
    Badge,
    Earned,
)
from django.http import JsonResponse
# from django.conf import settings

# time_zone = settings.TIME_ZONE

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

#  Number of points awarded for achieving each goal
POINTS_BADGE = 10
POINTS_SOLUTION = 10
POINTS_BONUS = 2


def add_points(question, profile, attempt):
    """
    Add appropriate number of points (if any) to user's profile after a question is answered.

    Adds points to a user's profile for when the user answers a question correctly for the first time. If the user
    answers the question correctly the first time they answer, the user gains bonus points.

    Subsequent correct answers should not award any points.
    """
    attempts = Attempt.objects.filter(question=question, profile=profile)
    is_first_correct = len(attempts.filter(passed_tests=True)) == 1
    points_to_add = 0

    # check if first passed
    if attempt.passed_tests and is_first_correct:
        points_to_add += POINTS_SOLUTION
        if len(attempts) == 1:
            # correct first try
            points_to_add += POINTS_BONUS

    profile.points += points_to_add
    profile.full_clean()
    profile.save()
    return profile.points


def save_goal_choice(request):
    """Update user's goal choice in database."""
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
    """
    Get the number of consecutive days with questions attempted.

    Gets all datetimes of attempts for the given user's profile, and checks for the longest continuous "streak" of
    days where attempts were made. Returns an integer of the longest attempt "streak".
    """
    # get datetimes from attempts in date form)
    attempts = Attempt.objects.filter(profile=user.profile).datetimes('datetime', 'day', 'DESC')

    if len(attempts) <= 0:
        return 0

    # first attempt is the start of the first streak
    streak = 1
    highest_streak = 0
    expected_date = attempts[0].date() - datetime.timedelta(days=1)

    for attempt in attempts[1:]:
        if attempt.date() == expected_date:
            # continue the streak
            streak += 1
        else:
            # streak has ended
            if streak > highest_streak:
                highest_streak = streak
            streak = 1
        # compare the next item to yesterday
        expected_date = attempt.date() - datetime.timedelta(days=1)

    if streak > highest_streak:
        highest_streak = streak

    return highest_streak


def get_questions_answered_in_past_month(user):
    """Get the number questions successfully answered in the past month."""
    today = datetime.datetime.now().replace(tzinfo=None) + relativedelta(days=1)
    last_month = today - relativedelta(months=1)
    solved = Attempt.objects.filter(profile=user.profile, datetime__gte=last_month.date(), passed_tests=True)
    return len(solved)


def check_badge_conditions(user):
    """
    Check if the user has earned new badges for their profile.

    Checks if the user has received each available badge. If not, check if the user has earned these badges. Badges
    available to be checked for are profile creation, number of attempts made, number of questions answered, and
    number of days with consecutive attempts.

    A badge will not be removed if the user had earned it before but now doesn't meet the conditions
    """
    user_attempts = Attempt.objects.filter(profile=user.profile)
    badge_objects = Badge.objects.all()
    earned_badges = user.profile.earned_badges.all()
    new_badge_names = ""
    new_badge_objects = []

    # account creation badge
    try:
        creation_badge = badge_objects.get(id_name="create-account")
        if creation_badge not in earned_badges:
            # create a new account creation
            Earned.objects.create(
                profile=user.profile,
                badge=creation_badge
            )
            new_badge_names = new_badge_names + "- " + creation_badge.display_name + "\n"
            new_badge_objects.append(creation_badge)
    except Badge.DoesNotExist:
        logger.warning("No such badge: create-account")
        pass

    # check questions solved badges
    try:
        question_badges = badge_objects.filter(id_name__contains="questions-solved")
        solved = user_attempts.filter(passed_tests=True)
        for question_badge in question_badges:
            if question_badge not in earned_badges:
                num_questions = int(question_badge.id_name.split("-")[2])
                if len(solved) >= num_questions:
                    Earned.objects.create(
                        profile=user.profile,
                        badge=question_badge
                    )
                    new_badge_names = new_badge_names + "- " + question_badge.display_name + "\n"
                    new_badge_objects.append(question_badge)
    except Badge.DoesNotExist:
        logger.warning("No such badges: questions-solved")
        pass

    # checked questions attempted badges
    try:
        attempt_badges = badge_objects.filter(id_name__contains="attempts-made")
        attempted = user_attempts
        for attempt_badge in attempt_badges:
            if attempt_badge not in earned_badges:
                num_questions = int(attempt_badge.id_name.split("-")[2])
                if len(attempted) >= num_questions:
                    Earned.objects.create(
                        profile=user.profile,
                        badge=attempt_badge
                    )
                    new_badge_names = new_badge_names + "- " + attempt_badge.display_name + "\n"
                    new_badge_objects.append(attempt_badge)
    except Badge.DoesNotExist:
        logger.warning("No such badges: attempts-made")
        pass

    # consecutive days logged in badges
    num_consec_days = get_days_consecutively_answered(user)
    consec_badges = badge_objects.filter(id_name__contains="consecutive-days")
    for consec_badge in consec_badges:
        if consec_badge not in earned_badges:
            n_days = int(consec_badge.id_name.split("-")[2])
            if n_days <= num_consec_days:
                Earned.objects.create(
                    profile=user.profile,
                    badge=consec_badge
                )
                new_badge_names = new_badge_names + "- " + consec_badge.display_name + "\n"
                new_badge_objects.append(consec_badge)

    new_points = calculate_badge_points(new_badge_objects)
    user.profile.points += new_points
    user.full_clean()
    user.save()
    return new_badge_names


def calculate_badge_points(badges):
    """Return the number of points earned by the user for new badges."""
    points = 0
    for badge in badges:
        points += badge.badge_tier * POINTS_BADGE
    return points


def backdate_points_and_badges():
    """Perform backdate of all points and badges for each profile in the system."""
    profiles = Profile.objects.all()
    num_profiles = len(profiles)
    for i in range(num_profiles):
        print("Backdating users: " + str(i + 1) + "/" + str(num_profiles), end="\r")
        profile = profiles[i]
        profile = backdate_badges(profile)
        profile = backdate_points(profile)
        # save profile when update is completed
        profile.full_clean()
        profile.save()
    print("\nBackdate complete.")


def backdate_points(profile):
    """Re-calculate points for the user profile."""
    questions = Question.objects.all()
    profile.points = 0
    for question in questions:
        user_attempts = Attempt.objects.filter(profile=profile, question=question)
        has_passed = len(user_attempts.filter(passed_tests=True)) > 0
        first_passed = False
        if len(user_attempts) > 0:
            first_passed = user_attempts[0].passed_tests
        if has_passed:
            profile.points += POINTS_SOLUTION
        if first_passed:
            profile.points += POINTS_BONUS
    for badge in profile.earned_badges.all():
        profile.points += POINTS_BADGE * badge.badge_tier
    return profile


def backdate_badges(profile):
    """Re-check the profile for badges earned."""
    check_badge_conditions(profile.user)
    return profile
