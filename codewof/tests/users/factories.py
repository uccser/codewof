"""Module for factories for tesing user application."""

from django.contrib.auth import get_user_model
import factory
from factory.django import DjangoModelFactory
from users.models import UserType


class UserFactory(DjangoModelFactory):
    """Factory for generating users."""

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("password")
    user_type = factory.Iterator(UserType.objects.all())

    class Meta:
        """Metadata for UserFactory class."""

        model = get_user_model()
