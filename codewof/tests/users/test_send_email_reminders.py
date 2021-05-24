import datetime
from io import StringIO

import pytz
from django.core.management import call_command
from django.test import TestCase
from django.utils.timezone import make_aware
from users.management.commands.send_email_reminders import Command
from codewof.tests.codewof_test_data_generator import generate_users_with_notifications, generate_users, \
    generate_questions, generate_attempts_no_defaults
from codewof.tests.conftest import user
from django.contrib.auth import get_user_model
from utils.Weekday import Weekday
from programming.models import Attempt, Question
from django.utils import timezone
from django.http import HttpResponse
from unittest.mock import patch
from django.core import mail

User = get_user_model()


def mocked_today_monday():
    # A Monday
    return datetime.datetime(2021, 5, 24, tzinfo=timezone.get_current_timezone())


def mocked_today_saturday():
    # A Saturday
    return datetime.datetime(2021, 5, 22, tzinfo=timezone.get_current_timezone())


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


class GetDaysSinceLastAttemptTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users(user)
        generate_questions()

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.question = Question.objects.get(slug='question-1')
        self.current_date = datetime.datetime(2020, 10, 21, tzinfo=timezone.get_current_timezone())

    def test_same_day_is_zero(self):
        attempt_date = datetime.datetime(2020, 10, 21, tzinfo=timezone.get_current_timezone())
        Attempt.objects.create(profile=self.user.profile, question=self.question, passed_tests=True,
                               datetime=attempt_date)
        days = Command().get_days_since_last_attempt(self.current_date, self.user)
        self.assertEqual(days, 0)

    def test_one_week_later_is_seven(self):
        attempt_date = datetime.datetime(2020, 10, 14, tzinfo=timezone.get_current_timezone())
        Attempt.objects.create(profile=self.user.profile, question=self.question, passed_tests=True,
                               datetime=attempt_date)
        days = Command().get_days_since_last_attempt(self.current_date, self.user)
        self.assertEqual(days, 7)

    def test_one_year_later_is_366(self):
        attempt_date = datetime.datetime(2019, 10, 21, tzinfo=timezone.get_current_timezone())
        Attempt.objects.create(profile=self.user.profile, question=self.question, passed_tests=True,
                               datetime=attempt_date)
        days = Command().get_days_since_last_attempt(self.current_date, self.user)
        self.assertEqual(days, 366)

    def test_current_date_before_attempt_date_is_invalid(self):
        attempt_date = datetime.datetime(2020, 10, 22, tzinfo=timezone.get_current_timezone())
        Attempt.objects.create(profile=self.user.profile, question=self.question, passed_tests=True,
                               datetime=attempt_date)
        self.assertRaises(ValueError, Command().get_days_since_last_attempt, self.current_date, self.user)

    def test_no_attempts_is_none(self):
        days = Command().get_days_since_last_attempt(self.current_date, self.user)
        self.assertIsNone(days)


class CreateMessageTests(TestCase):
    def test_zero_days_is_recent(self):
        message = Command().create_message(0)
        self.assertEqual(message, "You've been practicing recently. Keep it up!")

    def test_week_is_recent(self):
        message = Command().create_message(7)
        self.assertEqual(message, "You've been practicing recently. Keep it up!")

    def test_eight_days_is_awhile(self):
        message = Command().create_message(8)
        self.assertEqual(message, "It's been awhile since your last attempt. "
                                  "Remember to use CodeWOF regularly to keep your coding skills sharp.")

    def test_two_weeks_is_awhile(self):
        message = Command().create_message(14)
        self.assertEqual(message, "It's been awhile since your last attempt. "
                                  "Remember to use CodeWOF regularly to keep your coding skills sharp.")

    def test_fifteen_days_is_long_time(self):
        message = Command().create_message(15)
        self.assertEqual(message, "You haven't attempted a question in a long time. "
                                  "Try to use CodeWOF regularly to keep your coding skills sharp. "
                                  "If you don't want to use CodeWOF anymore, "
                                  "then click the link at the bottom of this email to stop getting reminders.")

    def test_no_attempts(self):
        message = Command().create_message(None)
        self.assertEqual(message, "You haven't attempted a question yet! "
                                  "Use CodeWOF regularly to keep your coding skills sharp."
                                  "If you don't want to use CodeWOF, "
                                  "then click the link at the bottom of this email to stop getting reminders.")


class BuildEmailHTMLTests(TestCase):
    def setUp(self):
        self.username = "User123"
        self.message = "A cool message"
        self.html = Command().build_email_html(self.username, self.message)
        self.response = HttpResponse(self.html)

    def test_html_contains_username(self):
        self.assertContains(self.response, "<p>Hi {},</p>".format(self.username), html=True)

    def test_html_contains_message(self):
        self.assertContains(self.response, "<p>{}</p>".format(self.message), html=True)


class BuildEmailPlainTests(TestCase):
    def setUp(self):
        self.username = "User123"
        self.message = "A cool message"
        self.plain = Command().build_email_plain(self.username, self.message)

    def test_plain_contains_username(self):
        self.assertTrue(self.username in self.plain)

    def test_plain_contains_message(self):
        self.assertTrue(self.message in self.plain)


class HandleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests - read only
        generate_users_with_notifications(user)
        generate_questions()
        generate_attempts_no_defaults()

    def setUp(self):
        self.john = User.objects.get(id=1)
        self.sally = User.objects.get(id=2)
        self.jane = User.objects.get(id=3)
        self.lazy = User.objects.get(id=4)
        self.brown = User.objects.get(id=5)

        self.no_attempts_message = Command().create_message(None)
        self.long_time_message = Command().create_message(15)
        self.recent_message = Command().create_message(1)
        self.awhile_message = Command().create_message(8)

        self.monday_outbox_sorted = self.get_monday_outbox_sorted()
        self.saturday_outbox_sorted = self.get_saturday_outbox_sorted()

    def call_command(self, *args, **kwargs):
        call_command(
            "send_email_reminders",
            *args,
            stdout=StringIO(),
            stderr=StringIO(),
            **kwargs,
        )

    @patch("users.management.commands.send_email_reminders.timezone.now", mocked_today_monday)
    def get_monday_outbox_sorted(self):
        self.call_command()
        result = sorted(mail.outbox, key=lambda x: x.to)
        mail.outbox = []
        return result

    @patch("users.management.commands.send_email_reminders.timezone.now", mocked_today_saturday)
    def get_saturday_outbox_sorted(self):
        self.call_command()
        result = sorted(mail.outbox, key=lambda x: x.to)
        mail.outbox = []
        return result

    # MONDAY TESTS
    def test_monday_notifies_three_users(self):
        self.assertEqual(len(self.monday_outbox_sorted), 3)

    def test_john_notified_on_monday_with_recent_message(self):
        self.assertTrue(self.john.first_name in self.monday_outbox_sorted[0].body)
        self.assertTrue(self.recent_message in self.monday_outbox_sorted[0].body)

    def test_sally_notified_on_monday_with_awhile_message(self):
        self.assertTrue(self.sally.first_name in self.monday_outbox_sorted[1].body)
        self.assertTrue(self.awhile_message in self.monday_outbox_sorted[1].body)

    def test_brown_notified_on_monday_with_no_attempts_message(self):
        self.assertTrue(self.brown.first_name in self.monday_outbox_sorted[2].body)
        self.assertTrue(self.no_attempts_message in self.monday_outbox_sorted[2].body)

    # SATURDAY TESTS
    def test_saturday_notifies_two_users(self):
        self.assertEqual(len(self.saturday_outbox_sorted), 2)

    def test_jane_notified_on_saturday_with_long_time_message(self):
        self.assertTrue(self.jane.first_name in self.saturday_outbox_sorted[0].body)
        self.assertTrue(self.long_time_message in self.saturday_outbox_sorted[0].body)

    def test_brown_notified_on_saturday_with_no_attempts_message(self):
        self.assertTrue(self.brown.first_name in self.saturday_outbox_sorted[1].body)
        self.assertTrue(self.no_attempts_message in self.saturday_outbox_sorted[1].body)
