from django.test import TestCase
from django.contrib.auth import get_user_model

from programming.models import (
    Question,
    Attempt,
    Achievement,
    Earned,
)
from tests.codewof_test_data_generator import (
    generate_users,
    generate_achievements,
    generate_questions,
    generate_attempts,
)
from programming.codewof_utils import (
    add_points,
    backdate_points,
    backdate_points_and_achievements,
    calculate_achievement_points,
    check_achievement_conditions,
    get_days_consecutively_answered,
    get_questions_answered_in_past_month,
    POINTS_ACHIEVEMENT,
    POINTS_SOLUTION,
)
from tests.conftest import user

User = get_user_model()


class TestCodewofUtils(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)
        generate_questions()
        generate_achievements()

    def test_add_points_first_attempt_correct(self):
        user = User.objects.get(id=1)
        question = Question.objects.get(slug='question-1')
        attempt = Attempt.objects.create(
            profile=user.profile,
            question=question,
            passed_tests=True
        )
        points_before = user.profile.points
        points_after = add_points(question, user.profile, attempt)
        self.assertEqual(points_after - points_before, POINTS_SOLUTION)

    def test_add_points_first_attempt_incorrect(self):
        user = User.objects.get(id=1)
        question = Question.objects.get(slug='question-1')
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

    def test_calculate_achievement_points_tier_0(self):
        achievement = Achievement.objects.get(id_name="create-account")
        achievements = [achievement]

        points = calculate_achievement_points(achievements)
        self.assertEqual(points, POINTS_ACHIEVEMENT * 0)

    def test_calculate_achievement_points_tier_1(self):
        achievement = Achievement.objects.get(id_name="questions-solved-1")
        achievements = [achievement]

        points = calculate_achievement_points(achievements)
        self.assertEqual(points, POINTS_ACHIEVEMENT * 1)

    def test_calculate_achievement_points_tier_2(self):
        achievement = Achievement.objects.get(id_name="attempts-made-5")
        achievements = [achievement]

        points = calculate_achievement_points(achievements)
        self.assertEqual(points, POINTS_ACHIEVEMENT * 2)

    def test_check_achievement_conditions(self):
        generate_attempts()
        user = User.objects.get(id=1)
        self.assertEqual(user.profile.earned_achievements.count(), 0)
        check_achievement_conditions(user.profile)
        earned_achievements = user.profile.earned_achievements
        self.assertTrue(earned_achievements.filter(id_name='create-account').exists())
        self.assertTrue(earned_achievements.filter(id_name='attempts-made-1').exists())
        self.assertTrue(earned_achievements.filter(id_name='attempts-made-5').exists())
        self.assertTrue(earned_achievements.filter(id_name='questions-solved-1').exists())
        self.assertTrue(earned_achievements.filter(id_name='consecutive-days-2').exists())

    def test_check_achievement_conditions_question_already_solved(self):
        generate_attempts()
        user = User.objects.get(id=1)
        self.assertEqual(user.profile.earned_achievements.count(), 0)
        check_achievement_conditions(user.profile)
        self.assertEqual(user.profile.earned_achievements.count(), 5)
        question = Question.objects.get(slug='program-question-1')

        # generate two more correct attempts for the SAME question
        # this would put the total number of correct submissions at 5
        # but since it's for the SAME question, it does not contribute to the questions solved achievement
        Attempt.objects.create(profile=user.profile, question=question, passed_tests=True)
        Attempt.objects.create(profile=user.profile, question=question, passed_tests=True)
        check_achievement_conditions(user.profile)
        earned_achievements = user.profile.earned_achievements
        self.assertFalse(earned_achievements.filter(id_name='questions-solved-5').exists())

    def test_check_achievement_conditions_questions_solved_does_not_exist(self):
        Achievement.objects.filter(id_name__contains="questions-solved").delete()
        generate_attempts()
        user = User.objects.get(id=1)
        check_achievement_conditions(user.profile)
        earned_achievements = user.profile.earned_achievements
        self.assertTrue(earned_achievements.filter(id_name='create-account').exists())
        self.assertTrue(earned_achievements.filter(id_name='attempts-made-1').exists())
        self.assertTrue(earned_achievements.filter(id_name='attempts-made-5').exists())
        self.assertTrue(earned_achievements.filter(id_name='consecutive-days-2').exists())
        # All questions-solved badges have been deleted and should not exist
        self.assertFalse(earned_achievements.filter(id_name='questions-solved-1').exists())

    def test_get_days_consecutively_answered(self):
        generate_attempts()
        user = User.objects.get(id=1)
        streak = get_days_consecutively_answered(user.profile)
        self.assertEqual(streak, 2)

    def test_get_questions_answered_in_past_month(self):
        generate_attempts()
        user = User.objects.get(id=1)
        num_solved = get_questions_answered_in_past_month(user.profile)
        self.assertEqual(num_solved, 1)

    def test_backdate_points_correct_second_attempt(self):
        user = User.objects.get(id=2)
        question = Question.objects.get(slug='question-1')
        Attempt.objects.create(profile=user.profile, question=question, passed_tests=False)
        Attempt.objects.create(profile=user.profile, question=question, passed_tests=True)
        profile = backdate_points(user.profile)
        self.assertEqual(profile.points, POINTS_SOLUTION)

    def test_backdate_points_correct_multiple_attempts(self):
        user = User.objects.get(id=2)
        question = Question.objects.get(slug='question-1')
        Attempt.objects.create(profile=user.profile, question=question, passed_tests=True)
        Attempt.objects.create(profile=user.profile, question=question, passed_tests=True)
        profile = backdate_points(user.profile)
        self.assertEqual(profile.points, POINTS_SOLUTION)

    def test_backdate_points_and_achievements_too_many_points(self):
        generate_attempts()
        user = User.objects.get(id=1)
        user.profile.points = 1000
        backdate_points_and_achievements()
        self.assertEqual(User.objects.get(id=1).profile.points, 60)

    def test_backdate_points_and_achievements_run_twice(self):
        generate_attempts()
        user = User.objects.get(id=1)
        user.profile.points = 1000
        backdate_points_and_achievements()
        backdate_points_and_achievements()
        self.assertEqual(User.objects.get(id=1).profile.points, 60)
        earned_achievements = User.objects.get(id=1).profile.earned_achievements
        self.assertEqual(len(earned_achievements.filter(id_name='create-account')), 1)
        self.assertEqual(len(earned_achievements.filter(id_name='attempts-made-1')), 1)
        self.assertEqual(len(earned_achievements.filter(id_name='attempts-made-5')), 1)
        self.assertEqual(len(earned_achievements.filter(id_name='questions-solved-1')), 1)
        self.assertEqual(len(earned_achievements.filter(id_name='consecutive-days-2')), 1)

    def test_backdate_points_and_achievements_achievement_earnt_no_longer_meets_requirements(self):
        user = User.objects.get(id=2)
        achievement = Achievement.objects.get(id_name='attempts-made-5')
        Earned.objects.create(profile=user.profile, achievement=achievement)
        backdate_points_and_achievements()
        self.assertTrue(
            User.objects.get(id=2).profile.earned_achievements.filter(id_name='attempts-made-5').exists()
        )
