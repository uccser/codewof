from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

from codewof.tests.codewof_test_data_generator import *
from codewof.tests.conftest import user

User = get_user_model()

from programming.models import Token, Badge, Question


class TokenModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Token.objects.create(name='sphere', token='abc')

    def test_name_unique(self):
        with self.assertRaises(IntegrityError):
            Token.objects.create(name='sphere', token='def')


class BadgeModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # generate_users()
        # generate_questions()
        generate_badges()
        # generate_attempts()

    def test_id_name_unique(self):
        with self.assertRaises(IntegrityError):
            Badge.objects.create(id_name='questions_solved_1', display_name='second', description='second')


class ProfileModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)

    def test_profile_starts_with_no_points(self):
        user = User.objects.get(id=1)
        points = user.profile.points
        self.assertEqual(points, 0)

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


class QuestionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_questions()

    def test_question_text_label(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('question_text').verbose_name
        self.assertEqual(field_label, 'question text')

    def test_solution_label(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('solution').verbose_name
        self.assertEqual(field_label, 'solution')

    def test_str_question_is_title(self):
        question = Question.objects.get(id=1)
        self.assertEqual(str(question), question.title)

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
