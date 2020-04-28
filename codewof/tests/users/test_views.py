import pytest
from django.test import Client, TestCase
from users.views import UserRedirectView, UserUpdateView
from codewof.tests.conftest import user

from codewof.tests.codewof_test_data_generator import generate_users, generate_badges
pytestmark = pytest.mark.django_db


class UserDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)

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


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
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
        generate_badges()

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
        resp = self.client.get('/users/achievements/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['badges_not_earned']), 10)
        self.assertEqual(resp.context['num_badges_earned'], 0)
        self.assertEqual(resp.context['num_badges'], 10)
