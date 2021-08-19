import datetime
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.utils import timezone

from django.test import TestCase
from tests.codewof_test_data_generator import generate_users, generate_groups, generate_invitations
from tests.conftest import user
from users.models import Invitation, Group

User = get_user_model()


def mocked_today():
    return datetime.datetime(2021, 10, 21, tzinfo=timezone.get_current_timezone())


class TestHandle(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)
        generate_groups()
        generate_invitations()

    def setUp(self):
        self.group_mystery = Group.objects.get(name="Group Mystery")
        self.group_team_300 = Group.objects.get(name="Team 300")
        self.group_team_cserg = Group.objects.get(name="Team CSERG")
        self.john = User.objects.get(pk=1)
        self.sally = User.objects.get(pk=2)
        self.invitation1 = Invitation.objects.get(email=self.john.email, group=self.group_team_300, inviter=self.sally)
        self.invitation2 = Invitation.objects.get(email="john@mail.com", group=self.group_mystery, inviter=self.sally)
        self.invitation3 = Invitation.objects.get(email=self.john.email, group=self.group_team_cserg,
                                                  inviter=self.sally)

    def call_command(self, *args, **kwargs):
        call_command(
            "remove_expired_invitations",
            *args,
            stdout=StringIO(),
            stderr=StringIO(),
            **kwargs,
        )

    @patch("users.management.commands.send_email_reminders.timezone.now", mocked_today)
    def test_removes_invitation_that_expired_yesterday(self):
        self.call_command()
        self.assertFalse(Invitation.objects.filter(pk=self.invitation3.pk))

    @patch("users.management.commands.send_email_reminders.timezone.now", mocked_today)
    def test_removes_invitation_that_expired_today(self):
        self.call_command()
        self.assertFalse(Invitation.objects.filter(pk=self.invitation1.pk))

    @patch("users.management.commands.send_email_reminders.timezone.now", mocked_today)
    def test_does_not_remove_invitation_that_expires_tomorrow(self):
        self.call_command()
        self.assertTrue(Invitation.objects.filter(pk=self.invitation2.pk))
