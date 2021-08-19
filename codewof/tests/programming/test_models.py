from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from programming.codewof_utils import check_achievement_conditions
from users.models import Group
from programming.models import (
    Token,
    Achievement,
    Question,
    Earned,
    Attempt,
    QuestionTypeProgram,
    QuestionTypeFunction,
    QuestionTypeParsons,
    QuestionTypeDebugging,
)

from tests.codewof_test_data_generator import (
    generate_users,
    generate_achievements,
    generate_questions,
    generate_attempts,
    generate_groups,
    generate_memberships,
    generate_likes
)
from tests.conftest import user

User = get_user_model()


class ProfileModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)
        generate_questions()
        generate_achievements()

    def test_profile_starts_with_no_points(self):
        user = User.objects.get(id=1)
        points = user.profile.points
        self.assertEqual(points, 0)

    def test_profile_starts_with_create_account_achievement(self):
        user = User.objects.get(id=1)
        check_achievement_conditions(user.profile)
        achievement = Achievement.objects.get(id_name="create-account")
        earned = Earned.objects.filter(profile=user.profile, achievement=achievement)
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
        self.assertEqual(str(user.profile), '{} {}'.format(user.first_name, user.last_name))


class AchievementModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)
        generate_achievements()

    def test_id_name_unique(self):
        with self.assertRaises(IntegrityError):
            Achievement.objects.create(
                id_name='questions-solved-1',
                display_name='second',
                description='second'
            )

    def test_achievement_tier_zero_default(self):
        achievement = Achievement.objects.create(
            id_name='achievement_name',
            display_name='Dummy Achievement',
            description='An achievement for testing'
        )
        self.assertEqual(achievement.achievement_tier, 0)

    def test_str_representation(self):
        achievement = Achievement.objects.get(id_name='questions-solved-1')
        self.assertEqual(str(achievement), achievement.display_name)

    def test_parent_achievement(self):
        achievement = Achievement.objects.get(id_name='attempts-made-1')
        parent_id = achievement.parent.id_name
        self.assertEqual(parent_id, 'attempts-made-5')

    def test_new_user_awards_create_account(self):
        user = User.objects.get(pk=1)
        check_achievement_conditions(user.profile)
        achievement = Achievement.objects.get(id_name="create-account")
        earned = Earned.objects.filter(profile=user.profile, achievement=achievement)
        self.assertEqual(len(earned), 1)

    def test_doesnt_award_twice_create_account(self):
        user = User.objects.get(pk=1)
        achievement = Achievement.objects.get(id_name="create-account")
        Earned.objects.create(profile=user.profile, achievement=achievement)
        check_achievement_conditions(user.profile)

        earned = Earned.objects.filter(profile=user.profile, achievement=achievement)
        self.assertEqual(len(earned), 1)

    def test_adding_unknown_achievement_doesnt_break(self):
        Achievement.objects.create(id_name="notrealachievement", display_name="test", description="test")
        user = User.objects.get(pk=1)
        check_achievement_conditions(user.profile)

    def test_award_solve_1_on_correct_attempt(self):
        user = User.objects.get(pk=1)
        question = Question.objects.create(title="Test question", question_text="Print hello world")
        Attempt.objects.create(profile=user.profile, question=question, passed_tests=True, user_code='')

        check_achievement_conditions(user.profile)
        achievement = Achievement.objects.get(id_name="questions-solved-1")
        earned = Earned.objects.filter(profile=user.profile, achievement=achievement)
        self.assertEqual(len(earned), 1)

    def test_not_award_solve_1_on_incorrect_attempt(self):
        user = User.objects.get(pk=1)
        question = Question.objects.create(title="Test question", question_text="Print hello world")
        Attempt.objects.create(profile=user.profile, question=question, passed_tests=False, user_code='')

        check_achievement_conditions(user.profile)
        achievement = Achievement.objects.get(id_name="questions-solved-1")
        earned = Earned.objects.filter(profile=user.profile, achievement=achievement)
        self.assertEqual(len(earned), 0)

    def test_queryset_ordering_questions_solved(self):
        questions_solved_achievements = Achievement.objects.filter(id_name__contains="questions-solved")
        self.assertQuerysetEqual(
            questions_solved_achievements,
            [
                '<Achievement: Solved one question>',
                '<Achievement: Solved five questions>',
                '<Achievement: Solved ten questions>',
                '<Achievement: Solved one hundred questions>',
            ]
        )

    def test_queryset_ordering_attempts_made(self):
        attempts_made_achievements = Achievement.objects.filter(id_name__contains="attempts-made")
        self.assertQuerysetEqual(
            attempts_made_achievements,
            [
                '<Achievement: One attempt made>',
                '<Achievement: Five attempts made>',
                '<Achievement: Ten attempts made>',
                '<Achievement: One hundred attempts made>',
            ]
        )


class EarnedModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        generate_users(user)
        generate_questions()
        generate_achievements()
        generate_attempts()

    def test_questions_solved_1_earnt(self):
        user = User.objects.get(id=1)
        check_achievement_conditions(user.profile)
        achievement = Achievement.objects.get(id_name="questions-solved-1")
        qs1_earned = Earned.objects.filter(profile=user.profile, achievement=achievement)
        self.assertEqual(len(qs1_earned), 1)

    def test_create_account_earnt(self):
        user = User.objects.get(id=1)
        check_achievement_conditions(user.profile)
        achievement = Achievement.objects.get(id_name="create-account")
        create_acc_earned = Earned.objects.filter(profile=user.profile, achievement=achievement)
        self.assertEqual(len(create_acc_earned), 1)

    def test_attempts_made_5_earnt(self):
        user = User.objects.get(id=1)
        check_achievement_conditions(user.profile)
        achievement = Achievement.objects.get(id_name="attempts-made-5")
        attempts_5_earned = Earned.objects.filter(profile=user.profile, achievement=achievement)
        self.assertEqual(len(attempts_5_earned), 1)

    def test_attempts_made_1_earnt(self):
        user = User.objects.get(id=1)
        check_achievement_conditions(user.profile)
        achievement = Achievement.objects.get(id_name="attempts-made-1")
        attempts1_earned = Earned.objects.filter(profile=user.profile, achievement=achievement)
        self.assertEqual(len(attempts1_earned), 1)

    def test_consecutive_days_2_earnt(self):
        user = User.objects.get(id=1)
        check_achievement_conditions(user.profile)
        achievement = Achievement.objects.get(id_name="consecutive-days-2")
        consec_days_earned = Earned.objects.filter(profile=user.profile, achievement=achievement)
        self.assertEqual(len(consec_days_earned), 1)


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


class QuestionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_questions()

    def test_question_slug_unique(self):
        with self.assertRaises(IntegrityError):
            Question.objects.create(
                slug='question-1',
                title='duplicate',
                question_text=''
            )

    def test_get_absolute_url(self):
        question = Question.objects.get(slug='question-1')
        url = question.get_absolute_url()
        self.assertEqual('/questions/{}/'.format(question.id), url)

    def test_str_representation(self):
        question = Question.objects.get(slug='question-1')
        self.assertEqual(str(question), question.title)

    def test_instance_of_question(self):
        question = Question.objects.get_subclass(slug='question-1')
        self.assertTrue(isinstance(question, Question))


class QuestionTypeProgramModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_questions()

    def test_question_type_program_instance(self):
        program_question = Question.objects.get_subclass(slug="program-question-1")
        self.assertTrue(isinstance(program_question, QuestionTypeProgram))

    def test_question_type_program_verbose_name(self):
        program_question = Question.objects.get_subclass(slug="program-question-1")
        self.assertEqual(program_question._meta.verbose_name, 'Program Question')

    def test_question_type_program_verbose_name_plural(self):
        program_question = Question.objects.get_subclass(slug="program-question-1")
        self.assertEqual(program_question._meta.verbose_name_plural, 'Program Questions')

    def test_str_representation(self):
        program_question = Question.objects.get_subclass(slug="program-question-1")
        self.assertEqual(
            str(program_question),
            '{}: {}'.format(program_question.QUESTION_TYPE, program_question.title)
        )


class QuestionTypeFunctionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_questions()

    def test_question_type_function_instance(self):
        function_question = Question.objects.get_subclass(slug="function-question-1")
        self.assertTrue(isinstance(function_question, QuestionTypeFunction))

    def test_question_type_function_verbose_name(self):
        function_question = Question.objects.get_subclass(slug="function-question-1")
        self.assertEqual(function_question._meta.verbose_name, 'Function Question')

    def test_question_type_function_verbose_name_plural(self):
        function_question = Question.objects.get_subclass(slug="function-question-1")
        self.assertEqual(function_question._meta.verbose_name_plural, 'Function Questions')

    def test_str_representation(self):
        function_question = Question.objects.get_subclass(slug="function-question-1")
        self.assertEqual(
            str(function_question),
            '{}: {}'.format(function_question.QUESTION_TYPE, function_question.title)
        )


class QuestionTypeParsonsModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_questions()

    def test_question_type_parsons_instance(self):
        parsons_question = Question.objects.get_subclass(slug="parsons-question-1")
        self.assertTrue(isinstance(parsons_question, QuestionTypeParsons))

    def test_question_type_parsons_verbose_name(self):
        parsons_question = Question.objects.get_subclass(slug="parsons-question-1")
        self.assertEqual(parsons_question._meta.verbose_name, 'Parsons Problem Question')

    def test_str_representation(self):
        parsons_question = Question.objects.get_subclass(slug="parsons-question-1")
        self.assertEqual(
            str(parsons_question),
            '{}: {}'.format(parsons_question.QUESTION_TYPE, parsons_question.title)
        )

    def test_lines_as_list(self):
        parsons_question = Question.objects.get_subclass(slug="parsons-question-1")
        lines_list = list(parsons_question.lines.split('\n'))
        shuffled_lines = parsons_question.lines_as_list()
        self.assertEqual(sorted(shuffled_lines), sorted(lines_list))


class QuestionTypeDebuggingModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_questions()

    def test_question_type_debugging_instance(self):
        debugging_question = Question.objects.get_subclass(slug="debugging-question-1")
        self.assertTrue(isinstance(debugging_question, QuestionTypeDebugging))

    def test_question_type_function_verbose_name(self):
        debugging_question = Question.objects.get_subclass(slug="debugging-question-1")
        self.assertEqual(debugging_question._meta.verbose_name, 'Debugging Problem Question')

    def test_str_representation(self):
        debugging_question = Question.objects.get_subclass(slug="debugging-question-1")
        self.assertEqual(
            str(debugging_question),
            '{}: {}'.format(debugging_question.QUESTION_TYPE, debugging_question.title)
        )

    def test_read_only_lines_top_default(self):
        debugging_question = Question.objects.get_subclass(slug="debugging-question-1")
        self.assertEqual(debugging_question.read_only_lines_top, 0)

    def test_read_only_lines_bottom_default(self):
        debugging_question = Question.objects.get_subclass(slug="debugging-question-1")
        self.assertEqual(debugging_question.read_only_lines_bottom, 0)


class AttemptModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)
        generate_questions()
        generate_attempts()
        generate_groups()
        generate_memberships()
        generate_likes()

    def test_get_like_users_for_group(self):
        attempt = Attempt.objects.first()
        group_north = Group.objects.get(name="Group North")
        self.assertEqual(len(attempt.get_like_users_for_group(group_north.pk)), 2)
