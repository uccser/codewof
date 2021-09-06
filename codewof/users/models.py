"""Models for user application."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone as django_timezone


class UserType(models.Model):
    """Group of a type of users on website."""

    slug = models.SlugField(
        unique=True,
    )
    name = models.CharField(
        max_length=50,
    )
    order = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        """Name of user type."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['order']


class User(AbstractUser):
    """User of website."""

    import pytz
    TIMEZONES = tuple((timezone, timezone.replace("_", " ")) for timezone in pytz.common_timezones)

    username = models.CharField(
        max_length=12,
        default='user',
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='first name',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='last name',
    )
    user_type = models.ForeignKey(
        UserType,
        related_name='users',
        on_delete=models.CASCADE,
    )

    # Which days of the week to get email reminders
    remind_on_monday = models.BooleanField(default=False)
    remind_on_tuesday = models.BooleanField(default=False)
    remind_on_wednesday = models.BooleanField(default=False)
    remind_on_thursday = models.BooleanField(default=False)
    remind_on_friday = models.BooleanField(default=False)
    remind_on_saturday = models.BooleanField(default=False)
    remind_on_sunday = models.BooleanField(default=False)

    # Determine when to send the email reminder
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='Pacific/Auckland')

    REMINDER_DAYS = [remind_on_monday, remind_on_tuesday, remind_on_wednesday, remind_on_thursday, remind_on_friday,
                     remind_on_saturday, remind_on_sunday]
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['first_name', 'user_type']

    def get_absolute_url(self):
        """Return URL for user's dashboard."""
        return reverse('users:dashboard')

    def __str__(self):
        """Label of the user."""
        return "{} {} ({})".format(self.first_name, self.last_name, self.email)

    def full_name(self):
        """Full name of the user."""
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        """Meta options for class."""

        ordering = ['first_name', 'last_name']


class Group(models.Model):
    """A collection of users who know each other."""

    name = models.CharField(
        max_length=50,
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    date_created = models.DateTimeField(default=django_timezone.now)
    users = models.ManyToManyField(User, through='Membership')
    feed_enabled = models.BooleanField(default=False)

    def __str__(self):
        """Label of the user."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['name']


class GroupRole(models.Model):
    """The role of the user in a group."""

    slug = models.SlugField(
        unique=True,
    )
    name = models.CharField(
        max_length=50,
    )
    order = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        """Name of group role."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['order']


class Membership(models.Model):
    """A class representing the relationship between a User and a Group."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.ForeignKey(
        GroupRole,
        related_name='memberships',
        on_delete=models.CASCADE,
    )
    date_joined = models.DateTimeField(default=django_timezone.now)


def get_default_invitation_expiry():
    """Calculate expiry date of invitation."""
    return django_timezone.now() + django_timezone.timedelta(days=7)


class Invitation(models.Model):
    """A class representing an invitation to join a Group."""

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    date_sent = models.DateTimeField(default=django_timezone.now)
    date_expires = models.DateTimeField(default=get_default_invitation_expiry)
