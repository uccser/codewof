from users.utils import send_invitation_email, create_invitation_plaintext, create_invitation_html
from tests.users.test_views import get_outbox_sorted
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.urls import reverse
from tests.conftest import user
from django.conf import settings

from tests.codewof_test_data_generator import (
    generate_users,
    generate_groups,
)

from users.models import Group

User = get_user_model()


class TestCreateInvitationPlaintext(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_groups()

    def setUp(self):
        self.john = User.objects.get(pk=1)
        self.sally = User.objects.get(pk=2)
        self.group_north = Group.objects.get(name="Group North")

    def test_user_exists(self):
        expected_url = settings.CODEWOF_DOMAIN + reverse('users:dashboard')
        expected = "Hi Sally,\n\nJohn Doe has invited you to join the Group 'Group North'. Click the link below to "\
                   "sign in. You will see your invitation in the dashboard, where you can join the group.\n\n{}"\
                   "\n\nThanks,\nThe Computer Science Education Research Group".format(expected_url)
        self.assertEqual(create_invitation_plaintext(True, self.sally.first_name,
                                                     self.john.first_name + " " + self.john.last_name,
                                                     self.group_north.name, self.sally.email),
                         expected)

    def test_user_does_not_exist(self):
        expected_url = settings.CODEWOF_DOMAIN + reverse('account_signup')
        expected = "Hi,\n\nJohn Doe has invited you to join the Group 'Group North'. CodeWOF helps you maintain your "\
                   "programming fitness with short daily programming exercises. With a free account you can save your"\
                   " progress and track your programming fitness over time. Click the link below to make an account,"\
                   " using the email unknown@mail.com. You will see your invitation in the dashboard, where you can "\
                   "join the group. If you already have a CodeWOF account, then add unknown@mail.com to your profile "\
                   "to make the invitation appear.\n\n{}\n\nThanks,\nThe Computer Science Education Research Group"\
            .format(expected_url)
        self.assertEqual(create_invitation_plaintext(False, None, self.john.first_name + " " + self.john.last_name,
                                                     self.group_north.name, "unknown@mail.com"), expected)


class TestCreateInvitationHTML(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_groups()

    def setUp(self):
        self.john = User.objects.get(pk=1)
        self.sally = User.objects.get(pk=2)
        self.group_north = Group.objects.get(name="Group North")

    def test_user_exists_html_contains_name(self):
        expected = "<p>Hi Sally,</p>"
        response = HttpResponse(create_invitation_html(True, self.sally.first_name,
                                                       self.john.first_name + " " + self.john.last_name,
                                                       self.group_north.name, self.sally.email))
        self.assertContains(response, expected, html=True)

    def test_user_exists_html_contains_correct_message(self):
        expected = "<p>John Doe has invited you to join the Group &#39;Group North&#39;. Click the link below to " \
                   "sign in. You will see your invitation in the dashboard, where you can join the group.</p>"
        response = HttpResponse(create_invitation_html(True, self.sally.first_name,
                                                       self.john.first_name + " " + self.john.last_name,
                                                       self.group_north.name, self.sally.email))
        self.assertContains(response, expected, html=True)

    def test_user_exists_html_contains_correct_link(self):
        expected_url = settings.CODEWOF_DOMAIN + reverse('users:dashboard')
        expected = f"<a href=\"{expected_url}\" style=\"color: #007bff; text-decoration: underline;\">Sign In</a>"
        response = HttpResponse(create_invitation_html(True, self.sally.first_name,
                                                       self.john.first_name + " " + self.john.last_name,
                                                       self.group_north.name, self.sally.email))
        self.assertContains(response, expected, html=True)

    def test_user_does_not_exist_html_contains_no_name(self):
        expected = "<p>Hi,</p>"
        response = HttpResponse(create_invitation_html(False, None, self.john.first_name + " " + self.john.last_name,
                                                       self.group_north.name, "unknown@mail.com"))
        self.assertContains(response, expected, html=True)

    def test_user_does_not_exist_html_contains_correct_message(self):
        expected = "<p>John Doe has invited you to join the Group &#39;Group North&#39;. CodeWOF helps you maintain "\
                   "your programming fitness with short daily programming exercises. With a free account you can "\
                   "save your progress and track your programming fitness over time. Click the link below to make an "\
                   "account, using the email unknown@mail.com. You will see your invitation in the dashboard, where "\
                   "you can join the group. If you already have a CodeWOF account, then add unknown@mail.com to your "\
                   "profile to make the invitation appear.</p>"
        response = HttpResponse(create_invitation_html(False, None, self.john.first_name + " " + self.john.last_name,
                                                       self.group_north.name, "unknown@mail.com"))
        self.assertContains(response, expected, html=True)

    def test_user_does_not_exist_html_contains_correct_link(self):
        expected_url = settings.CODEWOF_DOMAIN + reverse('account_signup')
        expected = f"<a href=\"{expected_url}\" style=\"color: #007bff; text-decoration: underline;\">Sign Up</a>"
        response = HttpResponse(create_invitation_html(False, None, self.john.first_name + " " + self.john.last_name,
                                                       self.group_north.name, "unknown@mail.com"))
        self.assertContains(response, expected, html=True)


class TestSendInvitationEmail(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_groups()

    def setUp(self):
        self.john = User.objects.get(pk=1)
        self.sally = User.objects.get(pk=2)
        self.group_north = Group.objects.get(name="Group North")

    def test_email_sent_user_exists(self):
        send_invitation_email(self.sally, self.john, self.group_north.name, self.sally.email)
        outbox = get_outbox_sorted()
        expected_url = settings.CODEWOF_DOMAIN + reverse('users:dashboard')
        expected = "Hi Sally,\n\nJohn Doe has invited you to join the Group 'Group North'. Click the link below to "\
                   "sign in. You will see your invitation in the dashboard, where you can join the group.\n\n{}"\
                   "\n\nThanks,\nThe Computer Science Education Research Group".format(expected_url)
        self.assertEqual(len(outbox), 1)
        self.assertTrue(self.sally.first_name in outbox[0].body)
        self.assertTrue(expected in outbox[0].body)

    def test_email_sent_user_does_not_exist(self):
        send_invitation_email(None, self.john, self.group_north.name, "unknown@mail.com")
        outbox = get_outbox_sorted()
        expected_url = settings.CODEWOF_DOMAIN + reverse('account_signup')
        expected = "Hi,\n\nJohn Doe has invited you to join the Group 'Group North'. CodeWOF helps you maintain your "\
                   "programming fitness with short daily programming exercises. With a free account you can save your"\
                   " progress and track your programming fitness over time. Click the link below to make an account,"\
                   " using the email unknown@mail.com. You will see your invitation in the dashboard, where you can "\
                   "join the group. If you already have a CodeWOF account, then add unknown@mail.com to your profile "\
                   "to make the invitation appear.\n\n{}\n\nThanks,\nThe Computer Science Education Research Group"\
            .format(expected_url)
        self.assertEqual(len(outbox), 1)
        self.assertTrue(expected in outbox[0].body)
