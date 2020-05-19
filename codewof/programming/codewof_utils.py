"""Utility functions for codeWOF system. Involves points, badges, and backdating points and badges per user."""

import datetime
import json
import logging
import time
import statistics
from dateutil.relativedelta import relativedelta

from programming.models import (
    Profile,
    Attempt,
    Badge,
    Earned,
)
from django.http import JsonResponse

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


def add_points(question, profile, attempt):
    """
    Add appropriate number of points (if any) to user profile after a question is answered.

    Subsequent correct answers should not award any points.
    """
    attempts = Attempt.objects.filter(question=question, profile=profile)
    is_first_correct = len(attempts.filter(passed_tests=True)) == 1

    if attempt.passed_tests and is_first_correct:
        profile.points += POINTS_SOLUTION

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


def get_days_consecutively_answered(profile, user_attempts=None):
    """
    Get the number of consecutive days with questions attempted.

    Gets all datetimes of attempts for the given user profile, and checks for the longest continuous "streak" of
    days where attempts were made. Returns an integer of the longest attempt "streak".
    """
    if user_attempts is None:
        user_attempts = Attempt.objects.filter(profile=profile)

    # get datetimes from attempts in date form)
    attempts = user_attempts.datetimes('datetime', 'day', 'DESC')

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


def get_questions_answered_in_past_month(profile, user_attempts=None):
    """Get the number questions successfully answered in the past month."""
    if user_attempts is None:
        user_attempts = Attempt.objects.filter(profile=profile)

    today = datetime.datetime.now().replace(tzinfo=None) + relativedelta(days=1)
    last_month = today - relativedelta(months=1)
    solved = user_attempts.filter(datetime__gte=last_month.date(), passed_tests=True)
    return len(solved)


def check_badge_conditions(profile, user_attempts=None):
    """
    Check if the user profile has earned new badges for their profile.

    Checks if the user has received each available badge. If not, check if the user has earned these badges. Badges
    available to be checked for are profile creation, number of attempts made, number of questions answered, and
    number of days with consecutive attempts.

    A badge will not be removed if the user had earned it before but now doesn't meet the conditions
    """
    if user_attempts is None:
        user_attempts = Attempt.objects.filter(profile=profile)

    badge_objects = Badge.objects.all()
    earned_badges = profile.earned_badges.all()
    new_badge_names = ""
    new_badge_objects = []

    # account creation badge
    try:
        creation_badge = badge_objects.get(id_name="create-account")
        if creation_badge not in earned_badges:
            # create a new account creation
            Earned.objects.create(
                profile=profile,
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
        solved = user_attempts.filter(passed_tests=True).distinct('question__slug')
        for question_badge in question_badges:
            if question_badge not in earned_badges:
                num_questions = int(question_badge.id_name.split("-")[2])
                if len(solved) >= num_questions:
                    Earned.objects.create(
                        profile=profile,
                        badge=question_badge
                    )
                    new_badge_names = new_badge_names + "- " + question_badge.display_name + "\n"
                    new_badge_objects.append(question_badge)
                else:
                    # hasn't achieved the current badge tier so won't achieve any higher ones
                    break
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
                        profile=profile,
                        badge=attempt_badge
                    )
                    new_badge_names = new_badge_names + "- " + attempt_badge.display_name + "\n"
                    new_badge_objects.append(attempt_badge)
                else:
                    # hasn't achieved the current badge tier so won't achieve any higher ones
                    break
    except Badge.DoesNotExist:
        logger.warning("No such badges: attempts-made")
        pass

    # consecutive days logged in badges
    num_consec_days = get_days_consecutively_answered(profile, user_attempts=user_attempts)
    consec_badges = badge_objects.filter(id_name__contains="consecutive-days")
    for consec_badge in consec_badges:
        if consec_badge not in earned_badges:
            n_days = int(consec_badge.id_name.split("-")[2])
            if n_days <= num_consec_days:
                Earned.objects.create(
                    profile=profile,
                    badge=consec_badge
                )
                new_badge_names = new_badge_names + "- " + consec_badge.display_name + "\n"
                new_badge_objects.append(consec_badge)
            else:
                # hasn't achieved the current badge tier so won't achieve any higher ones
                break

    new_points = calculate_badge_points(new_badge_objects)
    profile.points += new_points
    profile.full_clean()
    profile.save()
    return new_badge_names


def calculate_badge_points(badges):
    """Return the number of points earned by the user for new badges."""
    points = 0
    for badge in badges:
        points += badge.badge_tier * POINTS_BADGE
    return points


def backdate_user(profile):
    """Perform backdate of a single user profile."""
    attempts = Attempt.objects.filter(profile=profile)
    profile = backdate_badges(profile, user_attempts=attempts)
    profile = backdate_points(profile, user_attempts=attempts)
    profile.has_backdated = True
    profile.full_clean()
    profile.save()


def backdate_points_and_badges(n=-1, ignoreFlags=True):
    """Perform batch backdate of all points and badges for n profiles in the system."""
    backdate_badges_times = []
    backdate_points_times = []
    time_before = time.perf_counter()
    profiles = Profile.objects.all()
    if not ignoreFlags:
        profiles = profiles.filter(has_backdated=False)
    if (n > 0):
        profiles = profiles[:n]
    num_profiles = len(profiles)
    all_attempts = Attempt.objects.all()
    for i in range(num_profiles):
        # The commented out part below seems to break travis somehow
        print("Backdating user: {}/{}".format(str(i + 1), str(num_profiles)))  # , end="\r")
        profile = profiles[i]
        if not profile.has_backdated or ignoreFlags:
            attempts = all_attempts.filter(profile=profile)

            badges_time_before = time.perf_counter()
            profile = backdate_badges(profile, user_attempts=attempts)
            badges_time_after = time.perf_counter()
            backdate_badges_times.append(badges_time_after - badges_time_before)

            points_time_before = time.perf_counter()
            profile = backdate_points(profile, user_attempts=attempts)
            points_time_after = time.perf_counter()
            backdate_points_times.append(points_time_after - points_time_before)
            # save profile when update is completed
            profile.has_backdated = True
            profile.full_clean()
            profile.save()
        else:
            print("User {} has already been backdated".format(str(i + 1)))
    time_after = time.perf_counter()
    print("\nBackdate complete.")

    duration = time_after - time_before

    if len(backdate_badges_times) > 0 and len(backdate_points_times) > 0:
        badges_ave = statistics.mean(backdate_badges_times)
        logger.debug(f"Average time per user to backdate badges: {badges_ave:0.4f} seconds")

        points_ave = statistics.mean(backdate_points_times)
        logger.debug(f"Average time per user to backdate points: {points_ave:0.4f} seconds")

        average = duration / num_profiles
        logger.debug(f"Backdate duration {duration:0.4f} seconds, average per user {average:0.4f} seconds")
    else:
        logger.debug(f"No users were backdated")
        logger.debug(f"Backdate duration {duration:0.4f} seconds")


def backdate_points(profile, user_attempts=None):
    """Re-calculate points for the user profile."""
    if user_attempts is None:
        user_attempts = Attempt.objects.filter(profile=profile)

    num_correct_attempts = len(user_attempts.filter(passed_tests=True).distinct('question__slug'))
    profile.points = num_correct_attempts * POINTS_SOLUTION

    for badge in profile.earned_badges.all():
        profile.points += POINTS_BADGE * badge.badge_tier
    return profile


def backdate_badges(profile, user_attempts=None):
    """Re-check the profile for badges earned."""
    check_badge_conditions(profile, user_attempts=user_attempts)
    return profile
