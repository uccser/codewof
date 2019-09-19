"""
Class to generate test data required for testing codewof system

"""

from django.contrib.auth import get_user_model
from django.core.management import call_command
from datetime import datetime

from programming.models import Profile, Badge, Question, Attempt
from codewof.tests.users.factories import UserFactory
from codewof.tests.conftest import user

from users.models import UserType

User = get_user_model()


def generate_questions():
    Question.objects.create(title='Test', question_text='Hello')


def generate_users(user):
    # call_command("load_user_types")
    user.create_batch(size=2)
    # User.objects.create_user(username='john', email='john@uclive.ac.nz', password='onion', user_type=usertype)
    # User.objects.create_user(username='sally', email='sally@uclive.ac.nz', password='onion', user_type=usertype)


def generate_badges():
    Badge.objects.create(id_name='questions_solved_1', display_name='first', description='first')
    Badge.objects.create(id_name="create-account", display_name="test", description="test")
    Badge.objects.create(id_name="attempts-made-1", display_name="test", description="test")
    Badge.objects.create(id_name="attempts-made-5", display_name="test", description="test")
    Badge.objects.create(id_name="consecutive-days-2", display_name="test", description="test")


def generate_attempts():
    user = User.objects.get(id=1)
    question = Question.objects.get(id=1)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=True)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=False)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=False)
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=True, datetime=datetime.date(2019, 9, 9))
    Attempt.objects.create(profile=user.profile, question=question, passed_tests=True, datetime=datetime.date(2019, 9, 10))

