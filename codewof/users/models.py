"""Models for user application."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


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

    STUDENT = 1
    TEACHER = 2
    USER_TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES,
        default=STUDENT,
        blank=False,
    )

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['first_name', 'user_type']

    def get_absolute_url(self):
        """Return URL for user's webpage."""
        return reverse('users:profile')

    def __str__(self):
        """Name of the user."""
        return self.first_name

    def full_name(self):
        """Full name of the user."""
        return '{} {}'.format(self.first_name, self.last_name)
