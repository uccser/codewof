import datetime
from enum import Enum

import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone
from datetime import datetime
from users.models import User
from programming.models import Attempt
from utils.Weekday import Weekday
from django.template.loader import get_template
from django.template import Context
from django.urls import reverse
from django.contrib.sites.models import Site


class Command(BaseCommand):
    """Required command class for the custom Django load_user_types command."""

    def handle(self, *args, **options):
        """
        First obtains the list of Users who should get a reminder today. Sends an email to each user with a customised
        message based on recent usage.
        :param args:
        :param options:
        :return:
        """

        users_to_email = self.get_users_to_email()

        for user in users_to_email:
            days_since_last_attempt = self.get_days_since_last_attempt(timezone.now(), user)

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

    def get_users_to_email(self):
        """
        Obtains the collection of users to email. Iterates through each timezone, getting the day of the week for that
        timezone, then adding users that have opted to get a reminder in that timezone on that day.
        :return: A QuerySet of Users.
        """
        users_to_email = User.objects.none()
        for time_zone_string, _ in User.TIMEZONES:
            time_zone = pytz.timezone(time_zone_string)
            date_time = datetime.now(time_zone)
            weekday_num = Weekday(date_time.weekday())

            if weekday_num == Weekday.MONDAY:
                batch = User.objects.filter(remind_on_monday=True, timezone=time_zone_string)

            elif weekday_num == Weekday.TUESDAY:
                batch = User.objects.filter(remind_on_tuesday=True, timezone=time_zone_string)

            elif weekday_num == Weekday.WEDNESDAY:
                batch = User.objects.filter(remind_on_wednesday=True, timezone=time_zone_string)

            elif weekday_num == Weekday.THURSDAY:
                batch = User.objects.filter(remind_on_thursday=True, timezone=time_zone_string)

            elif weekday_num == Weekday.FRIDAY:
                batch = User.objects.filter(remind_on_friday=True, timezone=time_zone_string)

            elif weekday_num == Weekday.SATURDAY:
                batch = User.objects.filter(remind_on_saturday=True, timezone=time_zone_string)

            else:
                batch = User.objects.filter(remind_on_sunday=True, timezone=time_zone_string)

            if len(users_to_email) == 0:
                users_to_email = batch
            else:
                users_to_email = users_to_email.union(batch)

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
