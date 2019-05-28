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


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter for social accounts."""

    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        """Check if registrations are allowed for social accounts."""
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
