import datetime
import json

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.core import management
from django.core import mail
from django.urls import reverse
from users.views import UserRedirectView, UserUpdateView
from tests.conftest import user
from allauth.account.admin import EmailAddress

from tests.codewof_test_data_generator import (
    generate_users,
    generate_achievements,
    generate_attempts,
    generate_questions,
    generate_groups,
    generate_memberships,
    generate_email_accounts,
    generate_invitations,
    generate_invalid_invitations,
    generate_feed_attempts,
    generate_feed_attempts_failed_tests,
    generate_feed_attempts_non_member
)
from programming.codewof_utils import check_achievement_conditions
from programming.models import Achievement, Attempt
from users.models import Group, Membership, GroupRole, Invitation

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
        generate_email_accounts()
        generate_invitations()

    def setUp(self):
        self.client = Client()
        self.group_north = Group.objects.get(name="Group North")
        self.group_east = Group.objects.get(name="Group East")
        self.group_west = Group.objects.get(name="Group West")
        self.group_south = Group.objects.get(name="Group South")
        self.group_mystery = Group.objects.get(name="Group Mystery")
        self.group_team_300 = Group.objects.get(name="Team 300")
        self.group_team_cserg = Group.objects.get(name="Team CSERG")
        self.group_class_1 = Group.objects.get(name="Class 1")
        self.john = User.objects.get(pk=1)
        self.sally = User.objects.get(pk=2)
        self.membership1 = Membership.objects.get(user=self.john, group=self.group_north)
        self.membership2 = Membership.objects.get(user=self.john, group=self.group_east)
        self.membership3 = Membership.objects.get(user=self.john, group=self.group_west)
        self.membership4 = Membership.objects.get(user=self.john, group=self.group_south)
        self.invitation1 = Invitation.objects.get(email=self.john.email, group=self.group_team_300, inviter=self.sally)
        self.invitation2 = Invitation.objects.get(email="john@mail.com", group=self.group_mystery, inviter=self.sally)
        self.invitation3 = Invitation.objects.get(email=self.john.email, group=self.group_team_cserg,
                                                  inviter=self.sally)

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
        self.assertEqual(len(resp.context['all_achievements']), len(Achievement.objects.all()))
        self.assertEqual(resp.context['all_complete'], False)
        self.assertEqual(resp.context['codewof_profile'], user.profile)
        self.assertEqual(resp.context['goal'], user.profile.goal)
        self.assertEqual(resp.context['num_questions_answered'], 1)

    def test_context_object_memberships(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')

        self.assertEqual(len(resp.context['memberships']), 4)
        self.assertEqual(resp.context['memberships'][0], self.membership2)
        self.assertEqual(resp.context['memberships'][1], self.membership1)
        self.assertEqual(resp.context['memberships'][2], self.membership4)
        self.assertEqual(resp.context['memberships'][3], self.membership3)

    def test_context_object_invitations_in_correct_order(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        john_emails = EmailAddress.objects.filter(user=self.john)
        john_invitations = Invitation.objects.filter(email__in=john_emails.values('email'))

        self.assertEqual(len(john_invitations), 3)
        self.assertEqual(len(resp.context['invitations']), 3)
        self.assertEqual(resp.context['invitations'][0], self.invitation2)
        self.assertEqual(resp.context['invitations'][1], self.invitation1)
        self.assertEqual(resp.context['invitations'][2], self.invitation3)

    def test_context_object_invitations_is_missing_invalid_invitations(self):
        self.login_user()
        generate_invalid_invitations()
        resp = self.client.get('/users/dashboard/')
        john_emails = EmailAddress.objects.filter(user=self.john)
        john_invitations = Invitation.objects.filter(email__in=john_emails.values('email'))

        self.assertEqual(len(john_invitations), 6)
        self.assertEqual(set(resp.context['invitations']), {self.invitation1, self.invitation2, self.invitation3})

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
        self.assertContains(resp, "<h6 class=\"card-subtitle\">Group East is the best group.</h6>",
                            html=True)

    def test_view_contains_group_north_title(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h5 class=\"card-title\">Group North</h5>", html=True)

    def test_view_contains_group_north_subtitle(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h6 class=\"card-subtitle\">Group North is the best group.</h6>",
                            html=True)

    def test_view_contains_group_south_title(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h5 class=\"card-title\">Group South</h5>", html=True)

    def test_view_contains_group_south_subtitle(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h6 class=\"card-subtitle\">Group South is the best group.</h6>",
                            html=True)

    def test_view_contains_group_west_title(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h5 class=\"card-title\">Group West</h5>", html=True)

    def test_view_contains_group_west_subtitle(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<h6 class=\"card-subtitle\">Group West is the best group.</h6>",
                            html=True)

    def test_message_displayed_if_no_groups(self):
        self.login_user()
        User.objects.get(id=1).group_set.clear()
        resp = self.client.get('/users/dashboard/')
        self.assertContains(resp, "<p>You are not in any groups.</p>", html=True)
        self.assertQuerysetEqual(resp.context['memberships'], [])

    def test_view_contains_group_north_link(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        link = "<a class=\"card-link  stretched-link\" href=\"/users/groups/" + str(
            self.group_north.pk) + "/\">View</a>"
        self.assertContains(resp, link, html=True)

    def test_view_contains_group_east_link(self):
        self.login_user()
        resp = self.client.get('/users/dashboard/')
        link = "<a class=\"card-link  stretched-link\" href=\"/users/groups/" + str(self.group_east.pk) + \
               "/\">View</a>"
        self.assertContains(resp, link, html=True)


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

        assert view.get_success_url() == "/users/dashboard/"

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

        assert view.get_redirect_url() == "/users/dashboard/"


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
        management.call_command("load_group_roles")

    def setUp(self):
        self.client = Client()
        self.url = reverse('users:groups-add')

    def login_user(self):
        login = self.client.login(email='john@uclive.ac.nz', password='onion')
        self.assertTrue(login)

    # tests begin

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(self.url)
        self.assertRedirects(resp, '/accounts/login/?next=' + self.url)

    def test_view_url_exists(self):
        self.login_user()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login_user()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/group_form.html')

    def test_group_fields_are_correct(self):
        self.login_user()
        self.client.post(self.url, {'name': 'Cool Group', 'description': 'This is a cool group', 'feed_enabled': True})
        group = Group.objects.get(name='Cool Group')
        self.assertEqual(group.description, "This is a cool group")
        self.assertEqual(group.name, "Cool Group")
        self.assertTrue(group.feed_enabled)

    def test_2_groups_and_2_memberships_are_added_for_2_requests(self):
        self.login_user()
        self.client.post(self.url, {'name': 'Cool Group', 'description': 'This is a cool group', 'feed_enabled': True})
        self.client.post(self.url, {'name': 'Cool Group 2', 'description': 'This is another cool group',
                                    'feed_enabled': False})
        user = User.objects.get(id=1)
        group1 = Group.objects.get(name='Cool Group')
        group2 = Group.objects.get(name='Cool Group 2')
        membership1 = Membership.objects.get(group__name='Cool Group')
        membership2 = Membership.objects.get(group__name='Cool Group 2')

        self.assertEqual(len(user.group_set.all()), 2)
        self.assertEqual(len(user.membership_set.all()), 2)

        self.assertTrue(group1 in user.group_set.all())
        self.assertTrue(group2 in user.group_set.all())

        self.assertTrue(membership1 in user.membership_set.all())
        self.assertTrue(membership2 in user.membership_set.all())

    def test_group_is_not_added_if_name_is_empty(self):
        self.login_user()
        self.client.post(self.url, {'description': 'This is a group with no name'})
        user = User.objects.get(id=1)
        self.assertEqual(len(user.group_set.all()), 0)

    def test_group_is_added_if_description_is_empty(self):
        self.login_user()
        self.client.post(self.url, {'name': 'No Description Group'})
        user = User.objects.get(id=1)
        group = Group.objects.get(name='No Description Group')
        membership = Membership.objects.get(group__name='No Description Group')

        self.assertEqual(len(user.group_set.all()), 1)
        self.assertTrue(group in user.group_set.all())
        self.assertTrue(membership in user.membership_set.all())

    def test_feed_enabled_is_false_by_default_if_missing(self):
        self.login_user()
        self.client.post(self.url, {'name': 'Cool Group', 'description': 'This is a cool group'})
        group = Group.objects.get(name='Cool Group')
        self.assertFalse(group.feed_enabled)

    def test_redirects(self):
        self.login_user()
        resp = self.client.post(self.url, {'name': 'No Description Group'})
        self.assertRedirects(resp, '/users/dashboard/')

    def test_view_uses_correct_title(self):
        self.login_user()
        resp = self.client.get(self.url)
        self.assertContains(resp, "<h1>New Group</h1>", html=True)

    def test_view_uses_correct_button(self):
        self.login_user()
        resp = self.client.get(self.url)
        self.assertContains(resp, "<input class=\"btn btn-success\" type=\"submit\" value=\"Create Group\">",
                            html=True)


class TestGroupUpdateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_groups()
        generate_memberships()
        management.call_command("load_group_roles")

    def setUp(self):
        self.client = Client()
        self.group_north = Group.objects.get(name="Group North")
        self.group_east = Group.objects.get(name="Group East")
        self.group_west = Group.objects.get(name="Group West")
        self.group_south = Group.objects.get(name="Group South")
        self.group_mystery = Group.objects.get(name="Group Mystery")

    def login_user(self):
        login = self.client.login(email='john@uclive.ac.nz', password='onion')
        self.assertTrue(login)

    # tests begin

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('users:groups-edit', args=[self.group_north.pk]))
        self.assertRedirects(resp, '/accounts/login/?next=' + reverse('users:groups-edit', args=[self.group_north.pk]))

    def test_view_exists_if_admin(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-edit', args=[self.group_north.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_view_does_not_exist_if_member(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-edit', args=[self.group_east.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_view_does_not_exist_if_not_admin_or_member(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-edit', args=[self.group_mystery.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_view_uses_correct_template(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-edit', args=[self.group_north.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/group_form.html')

    def test_update_name_and_description(self):
        self.login_user()
        self.client.post(reverse('users:groups-edit', args=[self.group_north.pk]),
                         {'name': 'Group Up', 'description': 'Because Cardinal directions are too hard to remember.'})
        group_north_updated = Group.objects.get(pk=self.group_north.pk)
        self.assertEqual(group_north_updated.name, 'Group Up')
        self.assertEqual(group_north_updated.description, 'Because Cardinal directions are too hard to remember.')

    def test_group_is_not_modified_if_name_is_empty(self):
        self.login_user()
        self.client.post(reverse('users:groups-edit', args=[self.group_north.pk]),
                         {'description': 'This is a group with no name'})
        group_north_updated = Group.objects.get(pk=self.group_north.pk)
        self.assertEqual(group_north_updated.description, "Group North is the best group.")

    def test_group_is_modified_if_description_is_empty(self):
        self.login_user()
        self.client.post(reverse('users:groups-edit', args=[self.group_north.pk]), {'name': 'No Description Group'})
        group_north_updated = Group.objects.get(pk=self.group_north.pk)
        self.assertEqual(group_north_updated.name, 'No Description Group')

    def test_redirects(self):
        self.login_user()
        resp = self.client.post(reverse('users:groups-edit', args=[self.group_north.pk]),
                                {'name': 'No Description Group'})
        self.assertRedirects(resp, '/users/groups/' + str(self.group_north.pk) + '/')

    def test_view_contains_title(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-edit', args=[self.group_north.pk]))
        self.assertContains(resp, "<h1>Update Group</h1>", html=True)

    def test_view_uses_correct_button(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-edit', args=[self.group_north.pk]))
        self.assertContains(resp, "<input class=\"btn btn-success\" type=\"submit\" value=\"Edit Group\">", html=True)

    def test_cannot_edit_if_user_is_only_a_member(self):
        self.login_user()
        resp = self.client.post(reverse('users:groups-edit', args=[self.group_south.pk]),
                                {'name': 'Group Up',
                                 'description': 'Because Cardinal directions are too hard to remember.'})
        self.assertEqual(resp.status_code, 403)

    def test_cannot_edit_if_user_is_not_an_admin_or_a_member(self):
        self.login_user()
        resp = self.client.post(reverse('users:groups-edit', args=[self.group_mystery.pk]),
                                {'name': 'Group Infiltrate',
                                 'description': 'I infiltrated Group Mystery!.'})
        self.assertEqual(resp.status_code, 403)


class TestGroupDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_groups()
        generate_memberships()
        generate_questions()
        management.call_command("load_group_roles")

    def setUp(self):
        self.client = Client()
        self.group_north = Group.objects.get(name="Group North")
        self.group_east = Group.objects.get(name="Group East")
        self.group_west = Group.objects.get(name="Group West")
        self.group_south = Group.objects.get(name="Group South")
        self.group_mystery = Group.objects.get(name="Group Mystery")

    def login_user(self):
        login = self.client.login(email='john@uclive.ac.nz', password='onion')
        self.assertTrue(login)

    # tests begin

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertRedirects(resp,
                             '/accounts/login/?next=' + reverse('users:groups-detail', args=[self.group_north.pk]))

    def test_view_exists_if_admin(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_view_exists_if_member(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_east.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_view_does_not_exist_if_not_admin_or_member(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_mystery.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_view_uses_correct_template(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/group_detail.html')

    def test_view_displays_correct_group(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertContains(resp, "<h1>Group North</h1>", html=True)

    def test_view_displays_correct_description(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertContains(resp, "<p>Group North is the best group.</p>", html=True)

    def test_context_object_is_admin(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertEqual(resp.context['is_admin'], True)

    def test_context_object_is_member(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_east.pk]))
        self.assertEqual(resp.context['is_admin'], False)

    def test_context_object_has_own_membership(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertEqual(resp.context['user_membership'], Membership.objects.get(user=User.objects.get(pk=1),
                         group=self.group_north))

    def test_context_object_has_sorted_memberships(self):
        self.login_user()
        user_john = User.objects.get(id=1)
        user_sally = User.objects.get(id=2)
        user_alex = User.objects.get(id=3)
        membership_john = Membership.objects.get(user=user_john, group=self.group_north)
        membership_sally = Membership.objects.get(user=user_sally, group=self.group_north)
        membership_alex = Membership.objects.get(user=user_alex, group=self.group_north)
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertEqual(list(resp.context['memberships']), [membership_john, membership_alex, membership_sally])

    def test_context_object_has_roles(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        admin_role = GroupRole.objects.get(name="Admin")
        member_role = GroupRole.objects.get(name="Member")
        self.assertEqual(set(resp.context['roles']), {admin_role, member_role})

    def test_context_object_is_only_admin(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertTrue(resp.context['only_admin'])

    def test_context_object_member_is_not_only_admin(self):
        self.client.login(email='sally@uclive.ac.nz', password='onion')
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertFalse(resp.context['only_admin'])

    def test_context_object_is_not_only_admin(self):
        self.login_user()
        sally = User.objects.get(id=2)
        sally_membership = Membership.objects.get(user=sally, group=self.group_north.pk)
        admin_role = GroupRole.objects.get(name="Admin")
        sally_membership.role = admin_role
        sally_membership.save()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertFalse(resp.context['only_admin'])

    def test_context_has_sorted_feed(self):
        attempts = generate_feed_attempts()
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        feed = resp.context['feed']

        self.assertEqual(len(Attempt.objects.all()), 11)
        self.assertEqual(list(feed), sorted(attempts, key=lambda attempt: attempt.datetime, reverse=True)[:10])

    def test_context_feed_does_not_include_failed_attempts(self):
        attempts = generate_feed_attempts()
        generate_feed_attempts_failed_tests()
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        feed = resp.context['feed']

        self.assertEqual(len(Attempt.objects.all()), 14)
        attempts.remove(Attempt.objects.get(datetime=datetime.datetime(2020, 1, 1, 0, 0)))
        self.assertEqual(set(feed), set(attempts))

    def test_context_feed_does_not_include_non_member_attempts(self):
        attempts = generate_feed_attempts()
        generate_feed_attempts_non_member()
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        feed = resp.context['feed']

        self.assertEqual(len(Attempt.objects.all()), 13)
        attempts.remove(Attempt.objects.get(datetime=datetime.datetime(2020, 1, 1, 0, 0)))
        self.assertEqual(set(feed), set(attempts))

    def test_context_has_no_feed_if_disabled(self):
        generate_feed_attempts()
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_east.pk]))
        self.assertFalse('feed' in resp.context.keys())

    def test_has_edit_button_if_admin(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertContains(resp, "Edit Group")

    def test_has_delete_button_if_admin(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_north.pk]))
        self.assertContains(resp, "Delete Group")

    def test_has_no_edit_button_if_member(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_east.pk]))
        self.assertNotContains(resp, "Edit Group")

    def test_has_no_delete_button_if_member(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-detail', args=[self.group_east.pk]))
        self.assertNotContains(resp, "Delete Group")


class TestGroupDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_groups()
        generate_memberships()
        management.call_command("load_group_roles")

    def setUp(self):
        self.client = Client()
        self.group_north = Group.objects.get(name="Group North")
        self.group_east = Group.objects.get(name="Group East")
        self.group_west = Group.objects.get(name="Group West")
        self.group_south = Group.objects.get(name="Group South")
        self.group_mystery = Group.objects.get(name="Group Mystery")

    def login_user(self):
        login = self.client.login(email='john@uclive.ac.nz', password='onion')
        self.assertTrue(login)

    # tests begin

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('users:groups-delete', args=[self.group_north.pk]))
        self.assertRedirects(resp,
                             '/accounts/login/?next=' + reverse('users:groups-delete', args=[self.group_north.pk]))

    def test_view_exists_if_admin(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-delete', args=[self.group_north.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_view_does_not_exist_if_member(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-delete', args=[self.group_east.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_view_does_not_exist_if_not_admin_or_member(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-delete', args=[self.group_mystery.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_view_uses_correct_template(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-delete', args=[self.group_north.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/group_confirm_delete.html')

    def test_delete_group(self):
        self.login_user()
        groups_with_key = Group.objects.filter(pk=self.group_north.pk)
        self.assertEqual(len(groups_with_key), 1)
        self.client.post(reverse('users:groups-delete', args=[self.group_north.pk]))
        groups_with_key = Group.objects.filter(pk=self.group_north.pk)
        self.assertEqual(len(groups_with_key), 0)

    def test_delete_group_deletes_membership(self):
        self.login_user()
        user = User.objects.get(id=1)
        memberships = Membership.objects.filter(group=self.group_north, user=user)
        self.assertEqual(len(memberships), 1)
        self.client.post(reverse('users:groups-delete', args=[self.group_north.pk]))
        memberships = Membership.objects.filter(group=self.group_north, user=user)
        self.assertEqual(len(memberships), 0)

    def test_redirects(self):
        self.login_user()
        resp = self.client.post(reverse('users:groups-delete', args=[self.group_north.pk]))
        self.assertRedirects(resp, reverse('users:dashboard'))

    def test_view_contains_title(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-delete', args=[self.group_north.pk]))
        self.assertContains(resp, "<h1>Delete Group</h1>", html=True)

    def test_view_contains_correct_message(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-delete', args=[self.group_north.pk]))
        self.assertContains(resp, "<p>Are you sure you want to delete the Group 'Group North'?</p>", html=True)

    def test_view_contains_warning(self):
        self.login_user()
        resp = self.client.get(reverse('users:groups-delete', args=[self.group_north.pk]))
        self.assertContains(resp, "<p>There is no way to undo this action!</p>", html=True)

    def test_cannot_delete_if_user_is_only_a_member(self):
        self.login_user()
        resp = self.client.post(reverse('users:groups-delete', args=[self.group_south.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_cannot_delete_if_user_is_not_an_admin_or_a_member(self):
        self.login_user()
        resp = self.client.post(reverse('users:groups-delete', args=[self.group_mystery.pk]))
        self.assertEqual(resp.status_code, 403)


class TestAdminRequired(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_groups()
        generate_memberships()

    def setUp(self):
        self.client = Client()
        self.group_north = Group.objects.get(name="Group North")

    def login_user(self):
        login = self.client.login(email='john@uclive.ac.nz', password='onion')
        self.assertTrue(login)

    def test_invalid_id_is_500(self):
        self.login_user()
        body = json.dumps(
            {
                "memberships": [
                    {
                        "id": "string",
                        "delete": False,
                        "role": "Member"
                    }
                ]
            }
        )
        with self.assertRaisesMessage(Exception, "One of the membership objects has an id that is not an integer "
                                                 "(id=string)."):
            resp = self.client.put(reverse('users:groups-memberships-update', args=[self.group_north.pk]), body,
                                   content_type="application/json")
            self.assertEqual(resp.status_code, 500)

    def test_invalid_delete_is_500(self):
        self.login_user()
        body = json.dumps(
            {
                "memberships": [
                    {
                        "id": 1,
                        "delete": "True",
                        "role": "Member"
                    }
                ]
            }
        )
        with self.assertRaisesMessage(Exception, "One of the membership objects has delete value that is not a boolean"
                                                 " (id=1)."):
            resp = self.client.put(reverse('users:groups-memberships-update', args=[self.group_north.pk]), body,
                                   content_type="application/json")
            self.assertEqual(resp.status_code, 500)

    def test_invalid_role_is_500(self):
        self.login_user()
        membership = Membership.objects.all()[0]
        body = json.dumps(
            {
                "memberships": [
                    {
                        "id": membership.pk,
                        "delete": False,
                        "role": "Follower"
                    }
                ]
            }
        )
        with self.assertRaisesMessage(Exception, "One of the membership objects has a non-existent role "
                                                 "(id={}).".format(membership.pk)):
            resp = self.client.put(reverse('users:groups-memberships-update', args=[self.group_north.pk]), body,
                                   content_type="application/json")
            self.assertEqual(resp.status_code, 500)

    def test_membership_does_not_exist(self):
        self.login_user()
        body = json.dumps(
            {
                "memberships": [
                    {
                        "id": -1,
                        "delete": False,
                        "role": "Member"
                    }
                ]
            }
        )
        with self.assertRaises(ObjectDoesNotExist):
            resp = self.client.put(reverse('users:groups-memberships-update', args=[self.group_north.pk]), body,
                                   content_type="application/json")
            self.assertEqual(resp.status_code, 500)

    def test_delete_removes_membership(self):
        self.login_user()
        john = User.objects.get(pk=1)
        sally = User.objects.get(pk=2)
        alex = User.objects.get(pk=3)
        membership_to_remove = Membership.objects.get(group=self.group_north, user=sally)
        membership_to_keep = Membership.objects.get(group=self.group_north, user=john)
        membership_to_keep2 = Membership.objects.get(group=self.group_north, user=alex)
        self.assertEqual(set(self.group_north.membership_set.all()), {membership_to_remove, membership_to_keep,
                                                                      membership_to_keep2})

        body = json.dumps(
            {
                "memberships": [
                    {
                        "id": membership_to_remove.pk,
                        "delete": True,
                        "role": "Member"
                    }
                ]
            }
        )
        resp = self.client.put(reverse('users:groups-memberships-update', args=[self.group_north.pk]), body,
                               content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(set(self.group_north.membership_set.all()), {membership_to_keep, membership_to_keep2})

    def test_cannot_delete_if_last_admin(self):
        self.login_user()
        john = User.objects.get(pk=1)
        membership_to_remove = Membership.objects.get(group=self.group_north, user=john)

        body = json.dumps(
            {
                "memberships": [
                    {
                        "id": membership_to_remove.pk,
                        "delete": True,
                        "role": "Member"
                    }
                ]
            }
        )
        with self.assertRaisesMessage(Exception, "Must have at least one Admin in the group."):
            resp = self.client.put(reverse('users:groups-memberships-update', args=[self.group_north.pk]), body,
                                   content_type="application/json")
            self.assertEqual(resp.status_code, 500)

    def test_update_member_to_admin(self):
        self.login_user()
        sally = User.objects.get(pk=2)
        membership_to_update = Membership.objects.get(group=self.group_north, user=sally)
        self.assertEqual(membership_to_update.role, GroupRole.objects.get(name='Member'))

        body = json.dumps(
            {
                "memberships": [
                    {
                        "id": membership_to_update.pk,
                        "delete": False,
                        "role": "Admin"
                    }
                ]
            }
        )
        self.client.put(reverse('users:groups-memberships-update', args=[self.group_north.pk]), body,
                        content_type="application/json")
        membership_to_update = Membership.objects.get(group=self.group_north, user=sally)
        self.assertEqual(membership_to_update.role, GroupRole.objects.get(name='Admin'))

    def test_cannot_update_admin_to_member_if_last_admin(self):
        self.login_user()
        john = User.objects.get(pk=1)
        membership_to_update = Membership.objects.get(group=self.group_north, user=john)

        body = json.dumps(
            {
                "memberships": [
                    {
                        "id": membership_to_update.pk,
                        "delete": False,
                        "role": "Member"
                    }
                ]
            }
        )
        with self.assertRaisesMessage(Exception, "Must have at least one Admin in the group."):
            resp = self.client.put(reverse('users:groups-memberships-update', args=[self.group_north.pk]), body,
                                   content_type="application/json")
            self.assertEqual(resp.status_code, 500)

    def test_cannot_delete_all_admins_and_memberships_updates_are_undone(self):
        self.login_user()
        john = User.objects.get(pk=1)
        sally = User.objects.get(pk=2)
        john_membership = Membership.objects.get(group=self.group_north, user=john)
        sally_membership = Membership.objects.get(group=self.group_north, user=sally)
        admin_role = GroupRole.objects.get(name='Admin')
        sally_membership.role = admin_role
        sally_membership.save()
        self.assertEqual(set(Membership.objects.filter(group=self.group_north, role=admin_role)),
                         {john_membership, sally_membership})
        initial_memberships = Membership.objects.filter(group=self.group_north)

        body = json.dumps(
            {
                "memberships": [
                    {
                        "id": john_membership.pk,
                        "delete": True,
                        "role": "Admin"
                    },
                    {
                        "id": sally_membership.pk,
                        "delete": True,
                        "role": "Admin"
                    }
                ]
            }
        )
        with self.assertRaisesMessage(Exception, "Must have at least one Admin in the group."):
            resp = self.client.put(reverse('users:groups-memberships-update', args=[self.group_north.pk]), body,
                                   content_type="application/json")
            self.assertEqual(resp.status_code, 500)
            self.assertEqual(Membership.objects.filter(group=self.group_north), initial_memberships)

    def test_cannot_update_all_admins_to_members_and_memberships_updates_are_undone(self):
        self.login_user()
        john = User.objects.get(pk=1)
        sally = User.objects.get(pk=2)
        john_membership = Membership.objects.get(group=self.group_north, user=john)
        sally_membership = Membership.objects.get(group=self.group_north, user=sally)
        admin_role = GroupRole.objects.get(name='Admin')
        sally_membership.role = admin_role
        sally_membership.save()
        self.assertEqual(set(Membership.objects.filter(group=self.group_north, role=admin_role)),
                         {john_membership, sally_membership})
        initial_memberships = Membership.objects.filter(group=self.group_north)

        body = json.dumps(
            {
                "memberships": [
                    {
                        "id": john_membership.pk,
                        "delete": False,
                        "role": "Member"
                    },
                    {
                        "id": sally_membership.pk,
                        "delete": False,
                        "role": "Member"
                    }
                ]
            }
        )
        with self.assertRaisesMessage(Exception, "Must have at least one Admin in the group."):
            resp = self.client.put(reverse('users:groups-memberships-update', args=[self.group_north.pk]), body,
                                   content_type="application/json")
            self.assertEqual(resp.status_code, 500)
            self.assertEqual(Membership.objects.filter(group=self.group_north), initial_memberships)

    def test_empty_memberships_list_changes_nothing(self):
        self.login_user()
        initial_memberships = set(Membership.objects.filter(group=self.group_north))
        body = json.dumps(
            {
                "memberships": []
            }
        )
        resp = self.client.put(reverse('users:groups-memberships-update', args=[self.group_north.pk]), body,
                               content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(set(Membership.objects.filter(group=self.group_north)), initial_memberships)


class TestMembershipDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_groups()
        generate_memberships()
        management.call_command("load_group_roles")

    def setUp(self):
        self.client = Client()
        self.john = User.objects.get(pk=1)
        self.sally = User.objects.get(pk=2)
        self.group_north = Group.objects.get(name="Group North")
        self.john_north_membership = Membership.objects.get(group=self.group_north, user=self.john)
        self.sally_north_membership = Membership.objects.get(group=self.group_north, user=self.sally)

    def login_user(self, user):
        login = self.client.login(email=user.email, password='onion')
        self.assertTrue(login)

    # tests begin

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('users:groups-memberships-delete', args=[self.john_north_membership.pk]))
        self.assertRedirects(resp, '/accounts/login/?next=' + reverse('users:groups-memberships-delete',
                                                                      args=[self.john_north_membership.pk]))

    def test_view_exists_if_own_membership(self):
        self.login_user(self.sally)
        resp = self.client.get(reverse('users:groups-memberships-delete', args=[self.sally_north_membership.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_view_does_not_exist_if_other_membership(self):
        self.login_user(self.john)
        resp = self.client.get(reverse('users:groups-memberships-delete', args=[self.sally_north_membership.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_view_does_not_exist_if_insufficient_admins(self):
        self.login_user(self.john)
        with self.assertRaisesMessage(Exception, "A Group must have at least one Admin."):
            resp = self.client.get(reverse('users:groups-memberships-delete', args=[self.john_north_membership.pk]))
            self.assertEqual(resp.status_code, 500)

    def test_view_uses_correct_template(self):
        self.login_user(self.sally)
        resp = self.client.get(reverse('users:groups-memberships-delete', args=[self.sally_north_membership.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/membership_confirm_delete.html')

    def test_redirects(self):
        self.login_user(self.sally)
        resp = self.client.post(reverse('users:groups-memberships-delete', args=[self.sally_north_membership.pk]))
        self.assertRedirects(resp, reverse('users:dashboard'))

    def test_view_contains_title(self):
        self.login_user(self.sally)
        resp = self.client.get(reverse('users:groups-memberships-delete', args=[self.sally_north_membership.pk]))
        self.assertContains(resp, "<h1>Leave Group</h1>", html=True)

    def test_view_contains_correct_message(self):
        self.login_user(self.sally)
        resp = self.client.get(reverse('users:groups-memberships-delete', args=[self.sally_north_membership.pk]))
        self.assertContains(resp, "<p>Are you sure you want to leave the Group 'Group North'?</p>", html=True)

    def test_view_contains_warning(self):
        self.login_user(self.sally)
        resp = self.client.get(reverse('users:groups-memberships-delete', args=[self.sally_north_membership.pk]))
        self.assertContains(resp, "<p>You will have to be re-invited to view and participate in the Group again.</p>",
                            html=True)

    def test_admin_can_leave_if_other_admins(self):
        self.login_user(self.john)
        new_membership = self.sally_north_membership
        new_membership.role = GroupRole.objects.get(name='Admin')
        new_membership.save()
        self.client.post(reverse('users:groups-memberships-delete', args=[self.john_north_membership.pk]))
        self.assertEqual(len(Membership.objects.filter(group=self.group_north, user=self.john)), 0)

    def test_member_can_leave(self):
        self.login_user(self.sally)
        self.client.post(reverse('users:groups-memberships-delete', args=[self.sally_north_membership.pk]))
        self.assertEqual(len(Membership.objects.filter(group=self.group_north, user=self.sally)), 0)

    def test_cannot_leave_if_other_membership(self):
        self.login_user(self.john)
        resp = self.client.post(reverse('users:groups-memberships-delete', args=[self.sally_north_membership.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_cannot_leave_if_insufficient_admins(self):
        self.login_user(self.john)
        with self.assertRaisesMessage(Exception, "A Group must have at least one Admin."):
            resp = self.client.post(reverse('users:groups-memberships-delete', args=[self.john_north_membership.pk]))
            self.assertEqual(resp.status_code, 500)
            self.assertEqual(len(Membership.objects.filter(group=self.group_north, user=self.john)), 1)


def get_outbox_sorted():
    result = sorted(mail.outbox, key=lambda x: x.to)
    mail.outbox = []
    return result


class TestCreateInvitationsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_groups()
        generate_memberships()
        generate_email_accounts()
        management.call_command("load_group_roles")

    def setUp(self):
        self.john = User.objects.get(pk=1)
        self.sally = User.objects.get(pk=2)
        self.group_north = Group.objects.get(name="Group North")
        self.group_mystery = Group.objects.get(name="Group Mystery")
        self.client = Client()

    def login_user(self, user):
        login = self.client.login(email=user.email, password='onion')
        self.assertTrue(login)

    # tests begin

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('users:groups-memberships-invite', args=[self.group_north.pk]))
        self.assertRedirects(resp, '/accounts/login/?next=' + reverse('users:groups-memberships-invite',
                                                                      args=[self.group_north.pk]))

    def test_view_exists_if_admin(self):
        self.login_user(self.john)
        resp = self.client.get(reverse('users:groups-memberships-invite', args=[self.group_north.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_view_does_not_exist_if_not_admin(self):
        self.login_user(self.sally)
        resp = self.client.get(reverse('users:groups-memberships-invite', args=[self.group_north.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_view_does_not_exist_if_not_admin_or_member(self):
        self.login_user(self.john)
        resp = self.client.get(reverse('users:groups-memberships-invite', args=[self.group_mystery.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_view_uses_correct_template(self):
        self.login_user(self.john)
        resp = self.client.get(reverse('users:groups-memberships-invite', args=[self.group_north.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/create_invitations.html')

    def test_redirects(self):
        self.login_user(self.john)
        resp = self.client.post(reverse('users:groups-memberships-invite', args=[self.group_north.pk]),
                                {'emails': "test@mail.com"})
        self.assertRedirects(resp, reverse('users:groups-detail', args=[self.group_north.pk]))

    def test_cannot_post_if_member(self):
        self.login_user(self.sally)
        resp = self.client.post(reverse('users:groups-memberships-invite', args=[self.group_north.pk]),
                                {'emails': "test@mail.com"})
        self.assertEqual(resp.status_code, 403)

    def test_cannot_post_if_not_admin_or_member(self):
        self.login_user(self.sally)
        resp = self.client.post(reverse('users:groups-memberships-invite', args=[self.group_north.pk]),
                                {'emails': "test@mail.com"})
        self.assertEqual(resp.status_code, 403)

    def test_new_emails_only(self):
        self.login_user(self.john)
        emails = ['user1@mail.com', 'user2@mail.com', 'user3@mail.com']
        resp = self.client.post(reverse('users:groups-memberships-invite', args=[self.group_north.pk]),
                                {'emails': '\n'.join(emails)}, follow=True)
        messages = list(resp.context['messages'])
        outbox = get_outbox_sorted()

        self.assertEqual(len(outbox), 3)
        self.assertEqual(outbox[0].to[0], emails[0])
        self.assertEqual(outbox[1].to[0], emails[1])
        self.assertEqual(outbox[2].to[0], emails[2])
        self.assertTrue(Invitation.objects.filter(email=emails[0], group=self.group_north).exists())
        self.assertTrue(Invitation.objects.filter(email=emails[1], group=self.group_north).exists())
        self.assertTrue(Invitation.objects.filter(email=emails[2], group=self.group_north).exists())
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'The following emails had invitations sent to them: user1@mail.com, '
                                           'user2@mail.com, user3@mail.com')

    def test_existing_invitation(self):
        self.login_user(self.john)
        email = 'user1@mail.com'
        Invitation(email=email, group=self.group_north, inviter=self.john).save()
        resp = self.client.post(reverse('users:groups-memberships-invite', args=[self.group_north.pk]),
                                {'emails': email}, follow=True)
        messages = list(resp.context['messages'])
        outbox = get_outbox_sorted()

        self.assertEqual(len(outbox), 0)
        self.assertEqual(len(Invitation.objects.filter(email=email, group=self.group_north)), 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'The following emails were skipped either because they have already been '
                                           'invited or are already a member of the group: user1@mail.com')

    def test_existing_membership(self):
        self.login_user(self.john)
        resp = self.client.post(reverse('users:groups-memberships-invite', args=[self.group_north.pk]),
                                {'emails': self.sally.email}, follow=True)
        messages = list(resp.context['messages'])
        outbox = get_outbox_sorted()

        self.assertEqual(len(outbox), 0)
        self.assertFalse(Invitation.objects.filter(email=self.sally.email, group=self.group_north).exists())
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'The following emails were skipped either because they have already been '
                         'invited or are already a member of the group: ' + self.sally.email)

    def test_existing_invitation_to_different_email(self):
        self.login_user(self.sally)
        admin_role = GroupRole.objects.get(name="Admin")
        Membership(user=self.sally, group=self.group_mystery, role=admin_role).save()
        Invitation(email=self.john.email, group=self.group_mystery, inviter=self.sally).save()
        resp = self.client.post(reverse('users:groups-memberships-invite', args=[self.group_mystery.pk]),
                                {'emails': "john@mail.com"}, follow=True)
        messages = list(resp.context['messages'])
        outbox = get_outbox_sorted()
        john_emails = EmailAddress.objects.filter(user=self.john)
        john_invitations = Invitation.objects.filter(email__in=john_emails.values('email'), group=self.group_mystery)

        self.assertEqual(len(outbox), 0)
        self.assertEqual(len(john_invitations), 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'The following emails were skipped either because they have already been '
                         'invited or are already a member of the group: john@mail.com')

    def test_existing_invitation_to_different_email_in_same_request(self):
        self.login_user(self.sally)
        admin_role = GroupRole.objects.get(name="Admin")
        Membership(user=self.sally, group=self.group_mystery, role=admin_role).save()
        resp = self.client.post(reverse('users:groups-memberships-invite', args=[self.group_mystery.pk]),
                                {'emails': "john@mail.com\n" + self.john.email}, follow=True)
        messages = list(resp.context['messages'])
        outbox = get_outbox_sorted()
        john_emails = EmailAddress.objects.filter(user=self.john)
        john_invitations = Invitation.objects.filter(email__in=john_emails.values('email'), group=self.group_mystery)

        self.assertEqual(len(outbox), 1)
        self.assertEqual(outbox[0].to[0], "john@mail.com")
        self.assertEqual(len(john_invitations), 1)
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]),
                         'The following emails had invitations sent to them: john@mail.com')
        self.assertEqual(str(messages[1]),
                         'The following emails were skipped either because they have already been '
                         'invited or are already a member of the group: ' + self.john.email)

    def test_mix_of_new_emails_and_existing_invitations_and_existing_memberships(self):
        self.login_user(self.john)
        emails = ['user1@mail.com', 'user2@mail.com', self.sally.email, 'user3@mail.com']
        Invitation(email='user2@mail.com', group=self.group_north, inviter=self.john).save()
        resp = self.client.post(reverse('users:groups-memberships-invite', args=[self.group_north.pk]),
                                {'emails': '\n'.join(emails)}, follow=True)
        messages = list(resp.context['messages'])
        outbox = get_outbox_sorted()

        self.assertEqual(len(outbox), 2)
        self.assertEqual(outbox[0].to[0], emails[0])
        self.assertEqual(outbox[1].to[0], emails[3])
        self.assertTrue(Invitation.objects.filter(email=emails[0], group=self.group_north).exists())
        self.assertTrue(Invitation.objects.filter(email=emails[3], group=self.group_north).exists())
        self.assertEqual(len(Invitation.objects.filter(email=emails[1], group=self.group_north)), 1)
        self.assertFalse(Invitation.objects.filter(email=self.sally.email, group=self.group_north).exists())
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]),
                         'The following emails had invitations sent to them: user1@mail.com, user3@mail.com')
        self.assertEqual(str(messages[1]),
                         'The following emails were skipped either because they have already been '
                         'invited or are already a member of the group: user2@mail.com, ' + self.sally.email)

    def test_view_contains_title(self):
        self.login_user(self.john)
        resp = self.client.get(reverse('users:groups-memberships-invite', args=[self.group_north.pk]))
        self.assertContains(resp, "<h1>Send Invitations</h1>", html=True)


class TestAcceptInvitation(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_groups()
        generate_memberships()
        generate_invitations()
        generate_email_accounts()
        generate_invalid_invitations()

    def setUp(self):
        self.john = User.objects.get(pk=1)
        self.sally = User.objects.get(pk=2)
        self.group_mystery = Group.objects.get(name="Group Mystery")
        self.group_class_1 = Group.objects.get(name="Class 1")
        self.group_north = Group.objects.get(name="Group North")
        self.invitation = Invitation.objects.get(email="john@mail.com", group=self.group_mystery)
        self.invitation_already_member = Invitation.objects.get(email=self.john.email, group=self.group_north)
        self.invitation_unverified_email = Invitation.objects.get(email="jack@mail.com", group=self.group_class_1)
        self.client = Client()

    def login_user(self, user):
        login = self.client.login(email=user.email, password='onion')
        self.assertTrue(login)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.post(reverse('users:groups-invitations-accept', args=[self.invitation.pk]))
        self.assertRedirects(resp, '/accounts/login/?next=' + reverse('users:groups-invitations-accept',
                                                                      args=[self.invitation.pk]))

    def test_cannot_accept_if_other_invitation(self):
        self.login_user(self.sally)
        resp = self.client.post(reverse('users:groups-invitations-accept', args=[self.invitation.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_cannot_accept_if_email_unverified(self):
        self.login_user(self.john)
        resp = self.client.post(reverse('users:groups-invitations-accept', args=[self.invitation_unverified_email.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_can_accept_if_invitee(self):
        self.login_user(self.john)
        resp = self.client.post(reverse('users:groups-invitations-accept', args=[self.invitation.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_accepting_deletes_the_invitation(self):
        self.login_user(self.john)
        self.client.post(reverse('users:groups-invitations-accept', args=[self.invitation.pk]))
        self.assertFalse(Invitation.objects.filter(email="john@mail.com", group=self.group_mystery).exists())

    def test_accepting_deletes_duplicate_invitation(self):
        self.login_user(self.john)
        self.assertTrue(Invitation.objects.filter(email=self.john.email, group=self.group_mystery).exists())
        self.client.post(reverse('users:groups-invitations-accept', args=[self.invitation.pk]))
        self.assertFalse(Invitation.objects.filter(email=self.john.email, group=self.group_mystery).exists())

    def test_accepting_creates_membership(self):
        self.login_user(self.john)
        self.client.post(reverse('users:groups-invitations-accept', args=[self.invitation.pk]))
        member_role = GroupRole.objects.get(name="Member")
        self.assertTrue(Membership.objects.filter(user=self.john, group=self.group_mystery, role=member_role).exists())

    def test_accepting_invitation_when_user_is_already_a_member(self):
        self.login_user(self.john)
        self.assertEqual(len(Membership.objects.filter(user=self.john, group=self.group_north)), 1)
        self.client.post(reverse('users:groups-invitations-accept', args=[self.invitation_already_member.pk]))
        self.assertEqual(len(Membership.objects.filter(user=self.john, group=self.group_north)), 1)
        self.assertFalse(Invitation.objects.filter(email=self.john.email, group=self.group_north).exists())


class TestRejectInvitation(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_groups()
        generate_memberships()
        generate_invitations()
        generate_email_accounts()
        generate_invalid_invitations()

    def setUp(self):
        self.john = User.objects.get(pk=1)
        self.sally = User.objects.get(pk=2)
        self.group_mystery = Group.objects.get(name="Group Mystery")
        self.group_class_1 = Group.objects.get(name="Class 1")
        self.invitation = Invitation.objects.get(email="john@mail.com", group=self.group_mystery)
        self.invitation_unverified_email = Invitation.objects.get(email="jack@mail.com", group=self.group_class_1)
        self.client = Client()

    def login_user(self, user):
        login = self.client.login(email=user.email, password='onion')
        self.assertTrue(login)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.delete(reverse('users:groups-invitations-reject', args=[self.invitation.pk]))
        self.assertRedirects(resp, '/accounts/login/?next=' + reverse('users:groups-invitations-reject',
                                                                      args=[self.invitation.pk]))

    def test_cannot_reject_if_other_invitation(self):
        self.login_user(self.sally)
        resp = self.client.delete(reverse('users:groups-invitations-reject', args=[self.invitation.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_cannot_reject_if_email_unverified(self):
        self.login_user(self.john)
        resp = self.client.delete(reverse('users:groups-invitations-reject',
                                          args=[self.invitation_unverified_email.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_can_reject_if_invitee(self):
        self.login_user(self.john)
        resp = self.client.delete(reverse('users:groups-invitations-reject', args=[self.invitation.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_rejecting_deletes_the_invitation(self):
        self.login_user(self.john)
        self.client.delete(reverse('users:groups-invitations-reject', args=[self.invitation.pk]))
        self.assertFalse(Invitation.objects.filter(email="john@mail.com", group=self.group_mystery).exists())

    def test_rejecting_deletes_duplicate_invitation(self):
        self.login_user(self.john)
        self.assertTrue(Invitation.objects.filter(email=self.john.email, group=self.group_mystery).exists())
        self.client.delete(reverse('users:groups-invitations-reject', args=[self.invitation.pk]))
        self.assertFalse(Invitation.objects.filter(email=self.john.email, group=self.group_mystery).exists())


class TestGetGroupEmails(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_groups()
        generate_memberships()

    def setUp(self):
        self.john = User.objects.get(pk=1)
        self.sally = User.objects.get(pk=2)
        self.alex = User.objects.get(pk=3)
        self.jane = User.objects.get(pk=4)
        self.group_north = Group.objects.get(name="Group North")
        self.client = Client()

    def login_user(self, user):
        login = self.client.login(email=user.email, password='onion')
        self.assertTrue(login)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('users:groups-emails', args=[self.group_north.pk]))
        self.assertRedirects(resp, '/accounts/login/?next=' + reverse('users:groups-emails',
                                                                      args=[self.group_north.pk]))

    def test_cannot_get_emails_if_not_member_or_admin(self):
        self.login_user(self.jane)
        resp = self.client.get(reverse('users:groups-emails', args=[self.group_north.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_admin_can_get_emails(self):
        self.login_user(self.john)
        resp = self.client.get(reverse('users:groups-emails', args=[self.group_north.pk]))
        self.assertEqual(set(json.loads(resp.content)['emails']), {self.john.email, self.sally.email, self.alex.email})

    def test_member_can_get_emails(self):
        self.login_user(self.sally)
        resp = self.client.get(reverse('users:groups-emails', args=[self.group_north.pk]))
        self.assertEqual(set(json.loads(resp.content)['emails']), {self.john.email, self.sally.email, self.alex.email})
