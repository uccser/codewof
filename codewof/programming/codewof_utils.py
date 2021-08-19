"""
Utility functions for codeWOF system.

Involves points, achievements, and backdating points and achievements per user.
"""

import datetime
import json
import logging
import time
import statistics
from dateutil.relativedelta import relativedelta

from programming.models import (
    Profile,
    Attempt,
    Achievement,
    Earned,
)
from django.http import JsonResponse

logger = logging.getLogger(__name__)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'incremental': True,
    'root': {
        'level': 'DEBUG',
    },
}

#  Number of points awarded for achieving each goal
POINTS_ACHIEVEMENT = 10
POINTS_SOLUTION = 10


def add_points(question, profile, attempt):
    """
    Add appropriate number of points (if any) to user profile after a question is answered.

    Adds points to a user's profile for when the user answers a question correctly for the first time.
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


def check_achievement_conditions(profile, user_attempts=None):
    """
    Check if the user profile has earned new achievements for their profile.

    Checks if the user has received each available achievement.
    If not, check if the user has earned these achievements.
    Achievements available to be checked for are profile creation, number of attempts made,
    number of questions answered, and number of days with consecutive attempts.

    An achievement will not be removed if the user had earned it before but now doesn't meet the conditions
    """
    if user_attempts is None:
        user_attempts = Attempt.objects.filter(profile=profile)

    achievement_objects = Achievement.objects.all()
    earned_achievements = profile.earned_achievements.all()
    new_achievement_names = ""
    new_achievement_objects = []

    # account creation achievement
    try:
        creation_achievement = achievement_objects.get(id_name="create-account")
        if creation_achievement not in earned_achievements:
            # create a new account creation
            Earned.objects.create(
                profile=profile,
                achievement=creation_achievement
            )
            new_achievement_names += creation_achievement.display_name + "\n"
            new_achievement_objects.append(creation_achievement)
    except Achievement.DoesNotExist:
        logger.warning("No such achievement: create-account")
        pass

    # check questions solved achievements
    try:
        question_achievements = achievement_objects.filter(id_name__contains="questions-solved")
        solved = user_attempts.filter(passed_tests=True).distinct('question__slug')
        for question_achievement in question_achievements:
            if question_achievement not in earned_achievements:
                num_questions = int(question_achievement.id_name.split("-")[2])
                if len(solved) >= num_questions:
                    Earned.objects.create(
                        profile=profile,
                        achievement=question_achievement
                    )
                    new_achievement_names += question_achievement.display_name + "\n"
                    new_achievement_objects.append(question_achievement)
                else:
                    # hasn't achieved the current achievement tier so won't achieve any higher ones
                    break
    except Achievement.DoesNotExist:
        logger.warning("No such achievements: questions-solved")
        pass

    # checked questions attempted achievements
    try:
        attempt_achievements = achievement_objects.filter(id_name__contains="attempts-made")
        attempted = user_attempts
        for attempt_achievement in attempt_achievements:
            if attempt_achievement not in earned_achievements:
                num_questions = int(attempt_achievement.id_name.split("-")[2])
                if len(attempted) >= num_questions:
                    Earned.objects.create(
                        profile=profile,
                        achievement=attempt_achievement
                    )
                    new_achievement_names += attempt_achievement.display_name + "\n"
                    new_achievement_objects.append(attempt_achievement)
                else:
                    # hasn't achieved the current achievement tier so won't achieve any higher ones
                    break
    except Achievement.DoesNotExist:
        logger.warning("No such achievements: attempts-made")
        pass

    # consecutive days logged in achievements
    num_consec_days = get_days_consecutively_answered(profile, user_attempts=user_attempts)
    consec_achievements = achievement_objects.filter(id_name__contains="consecutive-days")
    for consec_achievement in consec_achievements:
        if consec_achievement not in earned_achievements:
            n_days = int(consec_achievement.id_name.split("-")[2])
            if n_days <= num_consec_days:
                Earned.objects.create(
                    profile=profile,
                    achievement=consec_achievement
                )
                new_achievement_names += consec_achievement.display_name + "\n"
                new_achievement_objects.append(consec_achievement)
            else:
                # hasn't achieved the current achievement tier so won't achieve any higher ones
                break

    new_points = calculate_achievement_points(new_achievement_objects)
    profile.points += new_points
    profile.full_clean()
    profile.save()
    return new_achievement_names


def calculate_achievement_points(achievements):
    """Return the number of points earned by the user for new achievements."""
    points = 0
    for achievement in achievements:
        points += achievement.achievement_tier * POINTS_ACHIEVEMENT
    return points


def backdate_user(profile):
    """Perform backdate of a single user profile."""
    attempts = Attempt.objects.filter(profile=profile)
    profile = backdate_achievements(profile, user_attempts=attempts)
    profile = backdate_points(profile, user_attempts=attempts)
    profile.has_backdated = True
    profile.full_clean()
    profile.save()


def backdate_points_and_achievements(n=-1, ignore_flags=True):
    """Perform batch backdate of all points and achievements for n profiles in the system."""
    backdate_achievements_times = []
    backdate_points_times = []
    time_before = time.perf_counter()
    profiles = Profile.objects.all()
    if not ignore_flags:
        profiles = profiles.filter(has_backdated=False)
    if (n > 0):
        profiles = profiles[:n]
    num_profiles = len(profiles)
    all_attempts = Attempt.objects.all()
    for i in range(num_profiles):
        # The commented out part below seems to break travis somehow
        print("Backdating user: {}/{}".format(str(i + 1), str(num_profiles)))  # , end="\r")
        profile = profiles[i]
        if not profile.has_backdated or ignore_flags:
            attempts = all_attempts.filter(profile=profile)

            achievements_time_before = time.perf_counter()
            profile = backdate_achievements(profile, user_attempts=attempts)
            achievements_time_after = time.perf_counter()
            backdate_achievements_times.append(achievements_time_after - achievements_time_before)

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

    if len(backdate_achievements_times) > 0 and len(backdate_points_times) > 0:
        achievements_ave = statistics.mean(backdate_achievements_times)
        logger.info(f"Average time per user to backdate achievements: {achievements_ave:0.4f} seconds")

        points_ave = statistics.mean(backdate_points_times)
        logger.info(f"Average time per user to backdate points: {points_ave:0.4f} seconds")

        average = duration / num_profiles
        logger.info(f"Backdate duration {duration:0.4f} seconds, average per user {average:0.4f} seconds")
    else:
        logger.info("No users were backdated")
        logger.info(f"Backdate duration {duration:0.4f} seconds")


def backdate_points(profile, user_attempts=None):
    """Re-calculate points for the user profile."""
    if user_attempts is None:
        user_attempts = Attempt.objects.filter(profile=profile)

    num_correct_attempts = len(user_attempts.filter(passed_tests=True).distinct('question__slug'))
    profile.points = num_correct_attempts * POINTS_SOLUTION

    for achievement in profile.earned_achievements.all():
        profile.points += POINTS_ACHIEVEMENT * achievement.achievement_tier
    return profile


def backdate_achievements(profile, user_attempts=None):
    """Re-check the profile for achievements earned."""
    check_achievement_conditions(profile, user_attempts=user_attempts)
    return profile
