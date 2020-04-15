from django.test import TestCase
from django.contrib.auth import get_user_model

from programming.models import (
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
from programming.codewof_utils import (
    add_points,
    backdate_points,
    backdate_points_and_badges,
    calculate_badge_points,
    check_badge_conditions,
    get_days_consecutively_answered,
    get_questions_answered_in_past_month,
    POINTS_BADGE,
    POINTS_SOLUTION,
    POINTS_BONUS,
)
from codewof.tests.conftest import user

User = get_user_model()


class TestCodewofUtils(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)
        generate_questions()
        generate_badges()

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

    def test_calculate_badge_points_tier_0(self):
        user = User.objects.get(id=1)
        badge = Badge.objects.get(id_name="create-account")
        badges = [badge]

        points = calculate_badge_points(badges)
        self.assertEqual(points, 0)

    def test_calculate_badge_points_tier_1(self):
        user = User.objects.get(id=1)
        badge = Badge.objects.get(id_name="questions-solved-1")
        badges = [badge]

        points = calculate_badge_points(badges)
        self.assertEqual(points, 10)

    def test_calculate_badge_points_tier_2(self):
        user = User.objects.get(id=1)
        badge = Badge.objects.get(id_name="attempts-made-5")
        badges = [badge]

        points = calculate_badge_points(badges)
        self.assertEqual(points, 20)

    def test_check_badge_conditions(self):
        generate_attempts()
        user = User.objects.get(id=1)
        self.assertEqual(user.profile.earned_badges.count(), 0)
        check_badge_conditions(user)
        earned_badges = user.profile.earned_badges
        self.assertTrue(earned_badges.filter(id_name='create-account').exists())
        self.assertTrue(earned_badges.filter(id_name='attempts-made-1').exists())
        self.assertTrue(earned_badges.filter(id_name='attempts-made-5').exists())
        self.assertTrue(earned_badges.filter(id_name='questions-solved-1').exists())
        self.assertTrue(earned_badges.filter(id_name='consecutive-days-2').exists())

    def test_get_days_consecutively_answered(self):
        generate_attempts()
        user = User.objects.get(id=1)
        streak = get_days_consecutively_answered(user)
        self.assertEqual(streak, 2)

    def test_get_questions_answered_in_past_month(self):
        generate_attempts()
        user = User.objects.get(id=1)
        num_solved = get_questions_answered_in_past_month(user)
        self.assertEqual(num_solved, 1)

    def test_backdate_points_correct_second_attempt(self):
        user = User.objects.get(id=2)
        question = Question.objects.get(slug='question-1')
        Attempt.objects.create(profile=user.profile, question=question, passed_tests=False)
        Attempt.objects.create(profile=user.profile, question=question, passed_tests=True)
        profile = backdate_points(user.profile)
        self.assertEqual(profile.points, 10)

    def test_backdate_points_correct_multiple_attempts(self):
        user = User.objects.get(id=2)
        question = Question.objects.get(slug='question-1')
        Attempt.objects.create(profile=user.profile, question=question, passed_tests=True)
        Attempt.objects.create(profile=user.profile, question=question, passed_tests=True)
        profile = backdate_points(user.profile)
        self.assertEqual(profile.points, 12)

    def test_backdate_points_and_badges_too_many_points(self):
        generate_attempts()
        user = User.objects.get(id=1)
        user.profile.points = 1000
        backdate_points_and_badges()
        self.assertEqual(User.objects.get(id=1).profile.points, 62)

    def test_backdate_points_and_badges_run_twice(self):
        generate_attempts()
        user = User.objects.get(id=1)
        user.profile.points = 1000
        backdate_points_and_badges()
        backdate_points_and_badges()
        self.assertEqual(User.objects.get(id=1).profile.points, 62)
        earned_badges = User.objects.get(id=1).profile.earned_badges
        self.assertEqual(len(earned_badges.filter(id_name='create-account')), 1)
        self.assertEqual(len(earned_badges.filter(id_name='attempts-made-1')), 1)
        self.assertEqual(len(earned_badges.filter(id_name='attempts-made-5')), 1)
        self.assertEqual(len(earned_badges.filter(id_name='questions-solved-1')), 1)
        self.assertEqual(len(earned_badges.filter(id_name='consecutive-days-2')), 1)

    def test_backdate_points_and_badges_badge_earnt_no_longer_meets_requirements(self):
        user = User.objects.get(id=2)
        badge = Badge.objects.get(id_name='attempts-made-5')
        Earned.objects.create(profile=user.profile, badge=badge)
        backdate_points_and_badges()
        self.assertTrue(
            User.objects.get(id=2).profile.earned_badges.filter(id_name='attempts-made-5').exists()
        )
