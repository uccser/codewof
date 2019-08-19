"""Module for configuring pytest."""

import pytest
from django.conf import settings
from django.test import RequestFactory
from django.core import management
from tests.users.factories import UserFactory
from users.models import User, UserType


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    """Pytest setup for media storage."""
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(request):
    """Pytest setup for user model."""
    management.call_command('load_user_types')

    def fin():
        print("teardown")
        User.objects.all().delete()
        UserType.objects.all().delete()

    request.addfinalizer(fin)
    return UserFactory()


@pytest.fixture
def request_factory():
    """Pytest setup for factory."""
    return RequestFactory()
