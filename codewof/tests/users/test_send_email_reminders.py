from django.test import TestCase
from users.management.commands.send_email_reminders import Command
from codewof.tests.codewof_test_data_generator import generate_users_with_notifications
from codewof.tests.conftest import user
from django.contrib.auth import get_user_model
from utils.Weekday import Weekday

User = get_user_model()


class GetUsersToEmailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users_with_notifications(user)

    def setUp(self):
        self.john = User.objects.get(id=1)
        self.sally = User.objects.get(id=2)
        self.jane = User.objects.get(id=3)
        self.lazy = User.objects.get(id=4)
        self.brown = User.objects.get(id=5)

    def test_monday_returns_three_users(self):
        result = Command().get_users_to_email(Weekday.MONDAY)
        self.assertEqual({self.john, self.sally, self.brown}, set(result))

    def test_tuesday_returns_one_user(self):
        result = Command().get_users_to_email(Weekday.TUESDAY)
        self.assertEqual({self.brown}, set(result))

    def test_wednesday_returns_two_users(self):
        result = Command().get_users_to_email(Weekday.WEDNESDAY)
        self.assertEqual({self.sally, self.brown}, set(result))

    def test_thursday_returns_two_users(self):
        result = Command().get_users_to_email(Weekday.THURSDAY)
        self.assertEqual({self.john, self.brown}, set(result))

    def test_friday_returns_two_users(self):
        result = Command().get_users_to_email(Weekday.FRIDAY)
        self.assertEqual({self.sally, self.brown}, set(result))

    def test_saturday_returns_two_users(self):
        result = Command().get_users_to_email(Weekday.SATURDAY)
        self.assertEqual({self.jane, self.brown}, set(result))

    def test_sunday_returns_no_users(self):
        result = Command().get_users_to_email(Weekday.SUNDAY)
        self.assertEqual(set(), set(result))
