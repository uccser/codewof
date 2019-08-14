"""Application configuration for the chapters application."""

from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    """Configuration object for the chapters application."""

    name = "users"
    verbose_name = "Users"

    def ready(self):
        """Import signals upon intialising application."""
        import users.signals  # noqa F401
