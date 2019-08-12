import pytest
from django.conf import settings
from django.urls import reverse, resolve

pytestmark = pytest.mark.django_db


def test_detail():
    assert (
        reverse("users:profile")
        == f"/users/profile/"
    )
    assert resolve(f"/users/profile/").view_name == "users:profile"


def test_update():
    assert reverse("users:update") == "/users/update/"
    assert resolve("/users/update/").view_name == "users:update"


def test_redirect():
    assert reverse("users:redirect") == "/users/redirect/"
    assert resolve("/users/redirect/").view_name == "users:redirect"
