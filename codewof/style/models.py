"""Models for style checker application."""

from django.db import models


class Error(models.Model):
    """Model to track style checker error code counts."""

    language = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    count = models.PositiveIntegerField(default=0)
    original_message = models.TextField(blank=True)
    title_templated = models.BooleanField(default=False)
    # The following fields are stored as HTML
    title = models.TextField()
    solution = models.TextField()
    explanation = models.TextField()

    def __str__(self):
        """Text representation of an error."""
        return '{} - {}'.format(self.language, self.code)
