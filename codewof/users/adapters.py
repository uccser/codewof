"""Adapters for the user application."""

from typing import Any
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    """Custom adapter for normal accounts."""

    def is_open_for_signup(self, request: HttpRequest):
        """Check if registrations are allowed for normal accounts."""
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_user(self, request, user, form, commit=False):
        """Save a new `User` instance using information provided.

        Key difference to built in function is not commiting
        until user type is added.
        """
        user = super().save_user(request, user, form, False)
        user.user_type = form.cleaned_data.get('user_type')
        user.save()
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter for social accounts."""

    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        """Check if registrations are allowed for social accounts."""
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
