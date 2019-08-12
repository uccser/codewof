import pytest
from django.conf import settings

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user):
    assert user.get_absolute_url() == f"/users/profile/"
