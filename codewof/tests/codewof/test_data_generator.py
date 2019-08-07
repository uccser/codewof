"""
Class to generate test data required for testing codewof system

"""

from django.contrib.auth import get_user_model

from codewof.models import Profile, Badge, Question, Attempt

User = get_user_model()


def generate_questions():
    Question.objects.create(title='Test', question_text='Hello')


def generate_users():
    User.objects.create_user(username='john', email='john@uclive.ac.nz', password='onion')
    User.objects.create_user(username='sally', email='sally@uclive.ac.nz', password='onion')


def generate_badges():
    Badge.objects.create(id_name='questions_solved_1', display_name='first', description='first')
    Badge.objects.create(id_name="create-account", display_name="test", description="test")
    Badge.objects.create(id_name="attempts-made-1", display_name="test", description="test")
    Badge.objects.create(id_name="attempts-made-5", display_name="test", description="test")
    Badge.objects.create(id_name="consecutive-days-2", display_name="test", description="test")


def generate_attempts():
    user = User.objects.get(id=1)
    Attempt.objects.create()
