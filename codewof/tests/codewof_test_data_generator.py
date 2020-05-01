"""Class to generate test data required for testing codewof system."""

from django.contrib.auth import get_user_model
from django.core import management
import datetime

from programming.models import (
    Question,
    Attempt,
    Badge,
    QuestionTypeProgram,
    QuestionTypeFunction,
    QuestionTypeParsons,
    QuestionTypeDebugging,
    TestCase,
    QuestionTypeProgramTestCase,
)

from users.models import UserType

User = get_user_model()


def generate_questions():
    """Generate questions for use in codeWOF tests. Questions contain minimum information and complexity."""
    Question.objects.create(slug="question-1", title='Test', question_text='Hello')

    QuestionTypeProgram.objects.create(
        slug="program-question-1",
        title='Test',
        question_text='Hello',
        solution="question_answer"
    )

    QuestionTypeFunction.objects.create(
        slug="function-question-1",
        title='Test',
        question_text='Hello',
        solution="question_answer"
    )

    QuestionTypeParsons.objects.create(
        slug="parsons-question-1",
        title='Test',
        question_text='Hello',
        solution="question_answer",
        lines="These are\nthe lines"
    )

    QuestionTypeDebugging.objects.create(
        slug="debugging-question-1",
        title='Test',
        question_text='Hello',
        solution="question_answer",
        initial_code=''
    )


def generate_users(user):
    """Generate users for codeWOF tests. Creates two basic users for unit tests."""
    management.call_command("load_user_types")
    user_john = User.objects.create_user(
        id=1,
        username='john',
        first_name='John',
        last_name='Doe',
        email='john@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='student')
    )
    user_john.save()

    user_sally = User.objects.create_user(
        id=2,
        username='sally',
        first_name='Sally',
        last_name='Jones',
        email='sally@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='other')
    )
    user_sally.save()


def generate_badges():
    """Create badges for codeWOF tests. Badges created for each main current badge category."""
    Badge.objects.create(
        id_name='create-account',
        display_name='Account created',
        description='test',
        badge_tier=0,
    )
    # Questions solved badges
    Badge.objects.create(
        id_name='questions-solved-100',
        display_name='Solved one hundred questions',
        description='test',
        badge_tier=4,
    )
    Badge.objects.create(
        id_name='questions-solved-10',
        display_name='Solved ten questions',
        description='test',
        badge_tier=3,
        parent=Badge.objects.get(id_name='questions-solved-100')
    )
    Badge.objects.create(
        id_name='questions-solved-5',
        display_name='Solved five questions',
        description='test',
        badge_tier=2,
        parent=Badge.objects.get(id_name='questions-solved-10')
    )
    Badge.objects.create(
        id_name='questions-solved-1',
        display_name='Solved one question',
        description='first',
        badge_tier=1,
        parent=Badge.objects.get(id_name='questions-solved-5')
    )
    # Attempts made badges
    Badge.objects.create(
        id_name='attempts-made-100',
        display_name='One hundred attempts made',
        description='test',
        badge_tier=4,
    )
    Badge.objects.create(
        id_name='attempts-made-10',
        display_name='Ten attempts made',
        description='test',
        badge_tier=3,
        parent=Badge.objects.get(id_name='attempts-made-100')
    )
    Badge.objects.create(
        id_name='attempts-made-5',
        display_name='Five attempts made',
        description='test',
        badge_tier=2
    )
    Badge.objects.create(
        id_name='attempts-made-1',
        display_name='One attempt made',
        description='test',
        badge_tier=1,
        parent=Badge.objects.get(id_name='attempts-made-5')
    )
    # Only need one of the consecutive days badges
    Badge.objects.create(
        id_name='consecutive-days-2',
        display_name='Two consecutive days',
        description='test',
        badge_tier=1,
    )


def generate_attempts():
    """
    Generate attempts for codeWOF tests.

    Attempts are generated for user 1 and question 1, with attempts created to cover consecutive days, failed attempts,
    and passed attempts. These attempts cover the main requirements to gain all test badges.
    """
    user = User.objects.get(id=1)
    question = Question.objects.get(slug='program-question-1')
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=True)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=False)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=False)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2019, 9, 9))
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2019, 9, 10))


def generate_test_cases():
    question = QuestionTypeProgram.objects.get(slug='program-question-1')
    TestCase.objects.create()

    QuestionTypeProgramTestCase.objects.create(
        id=1,
        test_input="",
        question=question
    )
