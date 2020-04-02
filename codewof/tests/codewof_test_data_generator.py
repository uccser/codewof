"""Class to generate test data required for testing codewof system."""

from django.contrib.auth import get_user_model
from django.core import management
from datetime import datetime

from programming.models import Badge, Question, Attempt

from users.models import UserType

User = get_user_model()


def generate_questions():
    """Generate questions for use in codeWOF tests. Questions contain minimum information and complexity."""
    Question.objects.create(title='Test', question_text='Hello')


def generate_users(user):
    """Generate users for codeWOF tests. Creates two basic users for unit tests."""
    management.call_command("load_user_types")
    User.objects.create_user(
        id=1,
        username='john',
        email='john@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='student')
    )
    User.objects.create_user(
        id=2,
        username='sally',
        email='sally@uclive.ac.nz',
        password='onion',
        user_type=UserType.objects.get(slug='other')
    )


def generate_badges():
    """Create badges for codeWOF tests. Badges created for each main current badge category."""
    Badge.objects.create(id_name='questions_solved_1', display_name='first', description='first')
    Badge.objects.create(id_name="attempts-made-1", display_name="test", description="test")
    Badge.objects.create(id_name="attempts-made-5", display_name="test", description="test")
    Badge.objects.create(id_name="consecutive-days-2", display_name="test", description="test")


def generate_attempts():
    """
    Generate attempts for codeWOF tests.

    Attempts are generated for user 1 and question 1, with attempts created to cover consecutive days, failed attempts,
    and passed attempts. These attempts cover the main requirements to gain all test badges.
    """
    user = User.objects.get(id=1)
    question = Question.objects.get(id=1)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=True)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=False)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=False)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2019, 9, 9))
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=True,
                           datetime=datetime.date(2019, 9, 10))
