import pytest
from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import UserType, User

from codewof.tests.codewof_test_data_generator import generate_users, generate_badges, generate_questions, generate_attempts
from codewof.tests.conftest import user

User = get_user_model()

pytestmark = pytest.mark.django_db


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)

    def test_default_username(self):
        user = User.objects.create(
            id=3,
            first_name='Test',
            last_name='Case',
            email='testcase@email.com',
            password='password',
            user_type=UserType.objects.get(slug='other')
        )
        self.assertEqual(user.username, 'user' + str(user.id))

    def test_user_get_absolute_url(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.get_absolute_url(), '/users/dashboard/')

    def test_str_representation(self):
        user = User.objects.get(id=1)
        self.assertEqual(
            str(user),
            '{} {} ({})'.format(user.first_name, user.last_name, user.email)
        )

    def test_full_name_representation(self):
        user = User.objects.get(id=1)
        self.assertEqual(
            user.full_name(),
            '{} {}'.format(user.first_name, user.last_name)
        )
