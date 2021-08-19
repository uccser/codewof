import pytest
from django.urls import reverse, resolve

pytestmark = pytest.mark.django_db


def test_detail():
    assert (
        reverse("users:dashboard")
        == "/users/dashboard/"
    )
    assert resolve("/users/dashboard/").view_name == "users:dashboard"


def test_update():
    assert reverse("users:update") == "/users/update/"
    assert resolve("/users/update/").view_name == "users:update"


def test_redirect():
    assert reverse("users:redirect") == "/users/redirect/"
    assert resolve("/users/redirect/").view_name == "users:redirect"
