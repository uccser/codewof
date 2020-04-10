from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from programming.models import (
    Profile,
    Question,
    Attempt,
    Badge,
    Earned,
)
from codewof.tests.codewof_test_data_generator import (
    generate_users,
    generate_badges,
    generate_questions,
    generate_attempts,
)
from programming.codewof_utils import *
from codewof.tests.conftest import user

User = get_user_model()


class TestCodewofUtils(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)
        generate_questions()
        generate_badges()

    # Test add_points function
    def test_add_points_first_attempt_correct(self):
        user = User.objects.get(id=1)
        question = Question.objects.get(id=1)
        attempt = Attempt.objects.create(
            profile=user.profile,
            question=question,
            passed_tests=True
        )
        points_before = user.profile.points
        points_after = add_points(question, user.profile, attempt)
        self.assertEqual(points_after - points_before, POINTS_SOLUTION + POINTS_BONUS)

    def test_add_points_first_attempt_incorrect(self):
        user = User.objects.get(id=1)
        question = Question.objects.get(id=1)
        attempt_1 = Attempt.objects.create(
            profile=user.profile,
            question=question,
            passed_tests=False
        )
        points_before = user.profile.points
        points_after = add_points(question, user.profile, attempt_1)
        self.assertEqual(points_after - points_before, 0)

        attempt_2 = Attempt.objects.create(
            profile=user.profile,
            question=question,
            passed_tests=True
        )
        points_before = user.profile.points
        points_after = add_points(question, user.profile, attempt_2)
        self.assertEqual(points_after - points_before, POINTS_SOLUTION)

    # Test caluclate_badge_points function
    def test_calculate_badge_points_tier_0(self):
        user = User.objects.get(id=1)
        badge = Badge.objects.get(id_name="create-account")
        badges = [badge]

        points_before = user.profile.points
        calculate_badge_points(user, badges)
        self.assertEqual(user.profile.points - points_before, badge.badge_tier * POINTS_BADGE)

    def test_calculate_badge_points_tier_1(self):
        user = User.objects.get(id=1)
        badge = Badge.objects.get(id_name="questions-solved-1")
        badges = [badge]

        points_before = user.profile.points
        calculate_badge_points(user, badges)
        self.assertEqual(user.profile.points - points_before, badge.badge_tier * POINTS_BADGE)

    def test_calculate_badge_points_tier_2(self):
        user = User.objects.get(id=1)
        badge = Badge.objects.get(id_name="attempts-made-5")
        badges = [badge]

        points_before = user.profile.points
        calculate_badge_points(user, badges)
        self.assertEqual(user.profile.points - points_before, badge.badge_tier * POINTS_BADGE)

    # Test calculate_badge_conditions function
    def test_check_badge_conditions(self):

