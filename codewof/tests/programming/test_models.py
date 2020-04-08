from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from programming.models import Token, Badge, Question, Earned, Attempt
from programming.codewof_utils import check_badge_conditions

from codewof.tests.codewof_test_data_generator import generate_users, generate_badges, generate_questions, generate_attempts
from codewof.tests.conftest import user

User = get_user_model()


class ProfileModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)
        generate_questions()
        generate_badges()

    def test_profile_starts_with_no_points(self):
        user = User.objects.get(id=1)
        points = user.profile.points
        self.assertEqual(points, 0)

    def test_profile_starts_with_create_account_badge(self):
        user = User.objects.get(id=1)
        check_badge_conditions(user)
        badge = Badge.objects.get(id_name="create-account")
        earned = Earned.objects.filter(profile=user.profile, badge=badge)
        self.assertEqual(len(earned), 1)

    def test_attempted_questions(self):
        user = User.objects.get(id=1)
        generate_attempts()
        attempted_questions = Attempt.objects.filter(profile=user.profile)
        # generate_attempts in codewof_utils will generate 5 attempts for user 1
        self.assertEqual(len(attempted_questions), 5)

    def test_profile_starts_on_easiest_goal_level(self):
        user = User.objects.get(id=1)
        goal = user.profile.goal
        self.assertEqual(goal, 1)

    def test_set_goal_to_4(self):
        user = User.objects.get(id=2)
        user.profile.goal = 4
        user.profile.full_clean()
        user.profile.save()
        double_check_user = User.objects.get(id=2)
        self.assertEqual(double_check_user.profile.goal, 4)

    def test_cannot_set_goal_less_than_1(self):
        user = User.objects.get(id=2)
        with self.assertRaises(ValidationError):
            user.profile.goal = 0
            user.profile.full_clean()
            user.profile.save()
        double_check_user = User.objects.get(id=2)
        self.assertEqual(double_check_user.profile.goal, 1)

    def test_cannot_set_goal_greater_than_7(self):
        user = User.objects.get(id=2)
        with self.assertRaises(ValidationError):
            user.profile.goal = 8
            user.profile.full_clean()
            user.profile.save()
        double_check_user = User.objects.get(id=2)
        self.assertEqual(double_check_user.profile.goal, 1)

    def test_str_representation(self):
        user = User.objects.get(id=1)
        self.assertEqual(str(user.profile), 'John Doe')


class BadgeModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)
        generate_badges()

    def test_id_name_unique(self):
        with self.assertRaises(IntegrityError):
            Badge.objects.create(
                id_name='questions-solved-1',
                display_name='second',
                description='second'
            )

    def test_badge_tier_zero_default(self):
        badge = Badge.objects.create(
            id_name='badge_name',
            display_name='Dummy Badge',
            description='A badge for testing'
        )
        self.assertEqual(badge.badge_tier, 0)

    def test_str_representation(self):
        badge = Badge.objects.get(id_name='questions-solved-1')
        self.assertEqual(str(badge), 'first')

    def test_parent_badge(self):
        badge = Badge.objects.get(id_name='attempts-made-1')
        parent_id = badge.parent.id_name
        self.assertEqual(parent_id, 'attempts-made-5')

    def test_new_user_awards_create_account(self):
        user = User.objects.get(pk=1)
        check_badge_conditions(user)
        badge = Badge.objects.get(id_name="create-account")
        earned = Earned.objects.filter(profile=user.profile, badge=badge)
        self.assertEqual(len(earned), 1)

    # def test_doesnt_award_twice_create_account(self):
    #     user = User.objects.get(pk=1)
    #     badge = Badge.objects.get(id_name="create-account")
    #     Earned.objects.create(profile=user.profile, badge=badge)
    #     check_badge_conditions(user)

    #     earned = Earned.objects.filter(profile=user.profile, badge=badge)
    #     self.assertEqual(len(earned), 1)

    # def test_adding_unknown_badge_doesnt_break(self):
    #     Badge.objects.create(id_name="notrealbadge", display_name="test", description="test")
    #     user = User.objects.get(pk=1)
    #     check_badge_conditions(user)

    def test_award_solve_1_on_correct_attempt(self):
        user = User.objects.get(pk=1)
        question = Question.objects.create(title="Test question", question_text="Print hello world")
        attempt = Attempt.objects.create(profile=user.profile, question=question, passed_tests=True, user_code='')

        check_badge_conditions(user)
        badge = Badge.objects.get(id_name="questions-solved-1")
        earned = Earned.objects.filter(profile=user.profile, badge=badge)
        self.assertEqual(len(earned), 1)

    def test_not_award_solve_1_on_incorrect_attempt(self):
        user = User.objects.get(pk=1)
        question = Question.objects.create(title="Test question", question_text="Print hello world")
        attempt = Attempt.objects.create(profile=user.profile, question=question, passed_tests=False, user_code='')

        check_badge_conditions(user)
        badge = Badge.objects.get(id_name="questions-solved-1")
        earned = Earned.objects.filter(profile=user.profile, badge=badge)
        self.assertEqual(len(earned), 0)


class EarnedModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        generate_users(user)
        generate_questions()
        generate_badges()
        generate_attempts()

    def test_questions_solved_1_earnt(self):
        user = User.objects.get(id=1)
        badge = Badge.objects.get(id_name="questions-solved-1")
        qs1_earned = Earned.objects.filter(profile=user.profile, badge=badge)
        self.assertEqual(len(qs1_earned), 1)

    def test_create_account_earnt(self):
        user = User.objects.get(id=1)
        badge = Badge.objects.get(id_name="create-account")
        create_acc_earned = Earned.objects.filter(profile=user.profile, badge=badge)
        self.assertEqual(len(create_acc_earned), 1)

    def test_attempts_made_5_earnt(self):
        user = User.objects.get(id=1)
        badge = Badge.objects.get(id_name="attempts-made-5")
        attempts_5_earned = Earned.objects.filter(profile=user.profile, badge=badge)
        self.assertEqual(len(attempts_5_earned), 1)

    def test_attempts_made_1_earnt(self):
        user = User.objects.get(id=1)
        badge = Badge.objects.get(id_name="attempts-made-1")
        attempts1_earned = Earned.objects.filter(profile=user.profile, badge=badge)
        self.assertEqual(len(attempts1_earned), 1)

    # def test_consecutive_days_2_earnt(self):
    #     user = User.objects.get(id=1)
    #     badge = Badge.objects.get(id_name="consecutive-days-2")
    #     consec_days_earned = Earned.objects.filter(profile=user.profile, badge=badge)
    #     self.assertEqual(len(consec_days_earned), 1)


class TokenModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Token.objects.create(name='sphere', token='abc')

    def test_name_unique(self):
        with self.assertRaises(IntegrityError):
            Token.objects.create(name='sphere', token='def')

    def test_str_representation(self):
        token = Token.objects.get(name='sphere')
        self.assertEqual(str(token), 'sphere')


# class QuestionModelTests(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # never modify this object in tests - read only
#         generate_questions()

#     def test_question_text_label(self):
#         question = Question.objects.get(id=1)
#         field_label = question._meta.get_field('question_text').verbose_name
#         self.assertEqual(field_label, 'question text')

#     def test_solution_label(self):
#         question = Question.objects.get(id=1)
#         field_label = question._meta.get_field('solution').verbose_name
#         self.assertEqual(field_label, 'solution')

#     def test_str_question_is_title(self):
#         question = Question.objects.get(id=1)
#         self.assertEqual(str(question), question.title)

# class ProgrammingFunctionModelTests(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         ProgrammingFunction.objects.create(title='Hello', question_text="Hello", function_name="hello")
#
#     def test_instance_of_question(self):
#         question = Question.objects.get_subclass(id=1)
#         self.assertTrue(isinstance(question, Question))
#
#     def test_instance_of_programming(self):
#         question = Question.objects.get_subclass(id=1)
#         self.assertTrue(isinstance(question, Programming))
#
#     def test_instance_of_programmingfunction(self):
#         question = Question.objects.get_subclass(id=1)
#         self.assertTrue(isinstance(question, ProgrammingFunction))
#
#     def test_not_instance_of_buggy(self):
#         question = Question.objects.get_subclass(id=1)
#         self.assertFalse(isinstance(question, Buggy))
#
#     def test_not_instance_of_buggyfunction(self):
#         question = Question.objects.get_subclass(id=1)
#         self.assertFalse(isinstance(question, BuggyFunction))
#
#     def test_str_question_is_title(self):
#         question = Question.objects.get(id=1)
#         self.assertEquals(str(question), question.title)
#
#
# class BuggyModelTests(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Buggy.objects.create(title='Hello', question_text="Hello", buggy_program="hello")
#
#     def test_instance_of_question(self):
#         question = Question.objects.get_subclass(id=1)
#         self.assertTrue(isinstance(question, Question))
#
#     def test_not_instance_of_programming(self):
#         question = Question.objects.get_subclass(id=1)
#         self.assertFalse(isinstance(question, Programming))
#
#     def test_not_instance_of_programmingfunction(self):
#         question = Question.objects.get_subclass(id=1)
#         self.assertFalse(isinstance(question, ProgrammingFunction))
#
#     def test_instance_of_buggy(self):
#         question = Question.objects.get_subclass(id=1)
#         self.assertTrue(isinstance(question, Buggy))
#
#     def test_not_instance_of_buggyfunction(self):
#         question = Question.objects.get_subclass(id=1)
#         self.assertFalse(isinstance(question, BuggyFunction))
#
#     def test_str_question_is_title(self):
#         question = Question.objects.get(id=1)
#         self.assertEquals(str(question), question.title)
