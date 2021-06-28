"""Models for user application."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


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
