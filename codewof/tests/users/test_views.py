import pytest
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from users.views import UserRedirectView, UserUpdateView
from codewof.tests.conftest import user

from codewof.tests.codewof_test_data_generator import (
    generate_users,
    generate_achievements,
    generate_attempts,
    generate_questions,
    generate_groups,
    generate_memberships
)
from codewof.programming.codewof_utils import check_achievement_conditions
from programming.models import Achievement
from users.models import Group
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
        generate_groups()
        generate_memberships()

    def setUp(self):
        self.client = Client()
        self.group_north = Group.objects.get(name="Group North")
        self.group_east = Group.objects.get(name="Group East")
        self.group_west = Group.objects.get(name="Group West")
        self.group_south = Group.objects.get(name="Group South")


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

        # Test the number of memberships and that the memberships are in the correct order (by group name)
        self.assertEqual(len(resp.context['memberships']), 4)
        self.assertEqual(resp.context['memberships'][0].group, self.group_east)
        self.assertEqual(resp.context['memberships'][1].group, self.group_north)
        self.assertEqual(resp.context['memberships'][2].group, self.group_south)
        self.assertEqual(resp.context['memberships'][3].group, self.group_west)

    def test_view_contains_groups_title(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h2>Groups</h2>", html=True)

    def test_view_contains_group_east_title(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h5 class=\"card-title\">Group East</h5>", html=True)

    def test_view_contains_group_east_subtitle(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h6 class=\"card-subtitle mb-2 text-muted\">Group East is the best group.</h6>", html=True)

    def test_view_contains_group_north_title(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h5 class=\"card-title\">Group North</h5>", html=True)

    def test_view_contains_group_north_subtitle(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h6 class=\"card-subtitle mb-2 text-muted\">Group North is the best group.</h6>", html=True)

    def test_view_contains_group_south_title(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h5 class=\"card-title\">Group South</h5>", html=True)

    def test_view_contains_group_south_subtitle(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h6 class=\"card-subtitle mb-2 text-muted\">Group South is the best group.</h6>", html=True)

    def test_view_contains_group_west_title(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h5 class=\"card-title\">Group West</h5>", html=True)

    def test_view_contains_group_west_subtitle(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h6 class=\"card-subtitle mb-2 text-muted\">Group West is the best group.</h6>", html=True)

    def test_message_displayed_if_no_groups(self):
        self.login_user()
        User.objects.get(id=1).group_set.clear()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<p>You are not in any groups.</p>", html=True)
        self.assertQuerysetEqual(resp.context['memberships'], [])


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


class TestGroupCreateView(TestCase):
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
        resp = self.client.get('/users/group/add/')
        self.assertRedirects(resp, '/accounts/login/?next=/users/group/add/')

    def test_view_url_exists(self):
        self.login_user()
        resp = self.client.get('/users/group/add/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login_user()
        resp = self.client.get('/users/group/add/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/group_form.html')

    def test_group_is_not_added_if_name_is_empty(self):
        self.login_user()
        self.client.post('/users/group/add/', {'description': 'This is a group with no name'})
        user = User.objects.get(id=1)
        self.assertEqual(len(user.group_set.all()), 0)

