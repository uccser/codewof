import pytest
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from users.views import UserRedirectView, UserUpdateView
from codewof.tests.conftest import user

from codewof.tests.codewof_test_data_generator import (
    generate_users,
    generate_achievements,
    generate_attempts,
    generate_questions
)
from codewof.programming.codewof_utils import check_achievement_conditions
from programming.models import Achievement
pytestmark = pytest.mark.django_db
User = get_user_model()


class UserDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_achievements()
        generate_questions()
        generate_attempts()

    def setUp(self):
        self.client = Client()

    def login_user(self):
        login = self.client.login(email='john@uclive.ac.nz', password='onion')
        self.assertTrue(login)

    # tests begin

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/users/dashboard/')
        self.assertRedirects(resp, '/accounts/login/?next=/users/dashboard/')

    def test_view_url_exists(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/dashboard.html')

    def test_context_object(self):
        self.login_user()
        user = User.objects.get(id=1)
        check_achievement_conditions(user.profile)
        resp = self.client.get('/users/dashboard/')
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(resp.context['questions_to_do']), 2)
        self.assertEqual(len(resp.context['studies']), 0)
        self.assertEqual(len(resp.context['all_achievements']), len(Achievement.objects.all()))
        self.assertEqual(resp.context['all_complete'], False)
        self.assertEqual(resp.context['codewof_profile'], user.profile)
        self.assertEqual(resp.context['goal'], user.profile.goal)
        self.assertEqual(resp.context['num_questions_answered'], 1)


class TestUserUpdateView:
    """Extracting view initialization code as class-scoped fixture.

    Would be great if only pytest-django supported non-function-scoped
    fixture db access -- this is a work-in-progress for now:
    https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(self, user, request_factory):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user
        view.request = request

        assert view.get_success_url() == f"/users/dashboard/"

    def test_get_object(self, user, request_factory):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user
        view.request = request
        assert view.get_object() == user


class UserUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)

    def setUp(self):
        self.client = Client()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/users/update/')
        self.assertRedirects(resp, '/accounts/login/?next=/users/update/')

    def test_view_url_exists(self):
        self.client.login(email='john@uclive.ac.nz', password='onion')
        response = self.client.get("/users/update/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='john@uclive.ac.nz', password='onion')
        response = self.client.get('/users/update/')
        self.assertTemplateUsed(response, 'users/user_form.html')

    # Test HTML elements exist

    def test_main_title_exists(self):
        self.client.login(email='john@uclive.ac.nz', password='onion')
        response = self.client.get("/users/update/")
        self.assertContains(response, "<h1>Update your profile</h1>", html=True)

    def test_details_subtitle_exists(self):
        self.client.login(email='john@uclive.ac.nz', password='onion')
        response = self.client.get("/users/update/")
        self.assertContains(response, "<h2>Details</h2>", html=True)

    def test_emails_subtitle_exists(self):
        self.client.login(email='john@uclive.ac.nz', password='onion')
        response = self.client.get("/users/update/")
        self.assertContains(response, "<h2>Emails</h2>", html=True)

    def test_first_name_value(self):
        self.client.login(email='john@uclive.ac.nz', password='onion')
        response = self.client.get("/users/update/")
        user = User.objects.get(id=1)
        self.assertContains(response, user.first_name)

    def test_last_name_value(self):
        self.client.login(email='john@uclive.ac.nz', password='onion')
        response = self.client.get("/users/update/")
        user = User.objects.get(id=1)
        self.assertContains(response, user.last_name)

    def test_user_type(self):
        self.client.login(email='john@uclive.ac.nz', password='onion')
        response = self.client.get("/users/update/")
        user = User.objects.get(id=1)
        self.assertContains(response, user.user_type)


class TestUserRedirectView:

    def test_get_redirect_url(self, user, request_factory):
        view = UserRedirectView()
        request = request_factory.get("/fake-url")
        request.user = user
        view.request = request

        assert view.get_redirect_url() == f"/users/dashboard/"


class TestUserAchievementView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_achievements()

    def setUp(self):
        self.client = Client()

    def login_user(self):
        login = self.client.login(email='john@uclive.ac.nz', password='onion')
        self.assertTrue(login)

    # tests begin
    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/users/achievements/')
        self.assertRedirects(resp, '/accounts/login/?next=/users/achievements/')

    def test_view_url_exists(self):
        self.login_user()
        resp = self.client.get('/users/achievements/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login_user()
        resp = self.client.get('/users/achievements/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/achievements.html')

    def test_context_object(self):
        self.login_user()
        user = User.objects.get(id=1)
        check_achievement_conditions(user.profile)
        resp = self.client.get('/users/achievements/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['achievements_not_earned']), 9)
        self.assertEqual(resp.context['num_achievements_earned'], 1)
        self.assertEqual(resp.context['num_achievements'], 10)
