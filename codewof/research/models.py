"""Models for research application."""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class StudyRegistration(models.Model):
    """An registration for an research study."""

    datetime = models.DateTimeField(auto_now_add=True)
    send_study_results = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        related_name='registrations',
        on_delete=models.CASCADE
    )


class ResearchPermissions(models.Model):
    """Model for custom permissions."""

    class Meta:
        """Meta options for model."""

        managed = False  # No database table
        default_permissions = ()  # Disable CRUD permissions
        permissions = (
            ('research_early_access', 'Research early access'),
        )
