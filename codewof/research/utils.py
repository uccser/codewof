"""Utility functions for research application."""

from research import settings


def get_study_for_context():
    """Return study data for use in template rendering.

    Return:
        Dictionary of study data.
    """
    context = {
        'slug': settings.SLUG,
        'title': settings.TITLE,
        'start': settings.START_DATETIME,
        'end': settings.END_DATETIME,
    }
    return context
