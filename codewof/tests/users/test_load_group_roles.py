from io import StringIO

from django.test import TestCase
from users.models import GroupRole
from django.core import management


class RolesAreLoadedTests(TestCase):
    def setUp(self):
        management.call_command("load_group_roles")

    def test_two_roles_are_added(self):
        self.assertEqual(len(GroupRole.objects.all()), 2)

    def test_member_role_is_loaded(self):
        self.assertEqual(GroupRole.objects.get(name="Member").name, "Member")

    def test_admin_role_is_loaded(self):
        self.assertEqual(GroupRole.objects.get(name="Admin").name, "Admin")


class RolesAreNotLoadedIfCommandNotCalledTests(TestCase):
    def test_no_roles_if_command_not_called(self):
        self.assertEqual(len(GroupRole.objects.all()), 0)
