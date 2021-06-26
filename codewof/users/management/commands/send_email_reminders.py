import datetime
from enum import Enum

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone
from users.models import User
from programming.models import Attempt
from utils.Weekday import Weekday
from django.template.loader import get_template
from django.template import Context
from django.urls import reverse
from django.contrib.sites.models import Site


class Command(BaseCommand):
    """Required command class for the custom Django send_email_reminders command."""

    def handle(self, *args, **options):
        """
        Gets the current day of the week, then obtains the list of Users who should get a reminder today. Sends an
        email to each user with a customised message based on recent usage.
        :param args:
        :param options:
        :return:
        """

        today = timezone.now()
        weekday = Weekday(today.date().weekday())

        users_to_email = self.get_users_to_email(weekday)

        for user in users_to_email:
            days_since_last_attempt = self.get_days_since_last_attempt(today, user)

            message = self.create_message(days_since_last_attempt)
            html = self.build_email_html(user.first_name, message)
            body = self.build_email_plain(user.first_name, message)

            send_mail(
                'CodeWOF Reminder',
                body,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=html
            )

    def get_days_since_last_attempt(self, today, user):
        """
        Obtains the number of days between a specified date and the user's last attempt. The date should be the same or
        ahead of the last attempt date.
        :param today: Today's date.
        :param user: The User.
        :return: The number of days since their last attempt or None if the user has no attempts.
        """
        attempts_sorted_by_datetime = Attempt.objects.filter(profile=user.profile).order_by('-datetime')
        if len(attempts_sorted_by_datetime) == 0:
            return None

        date_of_last_attempt = attempts_sorted_by_datetime[0].datetime
        if today < date_of_last_attempt:
            raise ValueError("Specified date is behind the user's last attempt")
        return (today - date_of_last_attempt).days

    def build_email_html(self, username, message):
        """
        Constructs HTML for the email body using the email_reminder.html template.
        :param username: The string username to insert in the template.
        :param message: The string message to insert in the template.
        :return: The rendered HTML.
        """
        email_template = get_template("users/email_reminder.html")
        return email_template.render({"username": username, "message": message})

    def build_email_plain(self, username, message):
        return "Hi {},\n\n{}\nLet's practice!: {}\n\nThanks,\nThe Computer Science Education Research " \
               "Group\n\nYou received this email because you opted into reminders. You can change " \
               "your reminder settings here: {}."\
            .format(username, message, Site.objects.get_current().domain + reverse('users:dashboard'),
                    Site.objects.get_current().domain + reverse('users:update'))

    def get_users_to_email(self, weekday_num):
        """
        Gets a list of users that have opted to receive a reminder for the inputted day of the week
        :param weekday_num: The day of the week as an int.
        :return: A QuerySet of Users.
        """
        if weekday_num == Weekday.MONDAY:
            users_to_email = User.objects.filter(remind_on_monday=True)
        elif weekday_num == Weekday.TUESDAY:
            users_to_email = User.objects.filter(remind_on_tuesday=True)
        elif weekday_num == Weekday.WEDNESDAY:
            users_to_email = User.objects.filter(remind_on_wednesday=True)
        elif weekday_num == Weekday.THURSDAY:
            users_to_email = User.objects.filter(remind_on_thursday=True)
        elif weekday_num == Weekday.FRIDAY:
            users_to_email = User.objects.filter(remind_on_friday=True)
        elif weekday_num == Weekday.SATURDAY:
            users_to_email = User.objects.filter(remind_on_saturday=True)
        else:
            users_to_email = User.objects.filter(remind_on_sunday=True)
        return users_to_email

    def create_message(self, days_since_last_attempt):
        """
        Returns a unique message based on recent usage.
        :param days_since_last_attempt: The int days since their last attempt.
        :return: a string message.
        """
        if days_since_last_attempt is None:
            message = "You haven't attempted a question yet! " \
                      "Use CodeWOF regularly to keep your coding skills sharp." \
                      "If you don't want to use CodeWOF, " \
                      "then click the link at the bottom of this email to stop getting reminders."
        elif days_since_last_attempt <= 7:
            message = "You've been practicing recently. Keep it up!"
        elif days_since_last_attempt > 14:
            message = "You haven't attempted a question in a long time. " \
                      "Try to use CodeWOF regularly to keep your coding skills sharp. " \
                      "If you don't want to use CodeWOF anymore, " \
                      "then click the link at the bottom of this email to stop getting reminders."
        else:
            message = "It's been awhile since your last attempt. " \
                      "Remember to use CodeWOF regularly to keep your coding skills sharp."
        return message

