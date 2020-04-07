import pytest
from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import UserType, User

from codewof.tests.codewof_test_data_generator import generate_users, generate_badges, generate_questions, generate_attempts
from codewof.tests.conftest import user

User = get_user_model()

pytestmark = pytest.mark.django_db


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)

    # def test_user_get_absolute_url(user: settings.AUTH_USER_MODEL):
    #     assert user.get_absolute_url() == f"/users/dashboard/"

    def test_str_representation(self):
        user = User.objects.get(id=1)
        self.assertEqual(str(user), 'John Doe (john@uclive.ac.nz)')
