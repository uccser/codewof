"""Utilities for the style checker application."""

from django.db.models import F
from django.template.loader import render_to_string
from style.models import Error


def render_results_as_html(issues):
    """Render style issue data as HTML.

    Args:
        issues (list): List of style issues.

    Returns:
        HTML string.
    """
    result_html = render_to_string(
        'style/component/result.html',
        {
            'issues': issues,
            'issue_count': len(issues),
        }
    )
    return result_html


def render_results_as_text(user_code, issues):
    """Render style issue data as HTML.

    Args:
        user_code (str): String of user code.
        issues (list): List of style issues.

    Returns:
        String of text.
    """
    result_text = render_to_string(
        'style/component/result.txt',
        {
            'user_code': user_code,
            'issues': issues,
            'issue_count': len(issues),
        }
    )
    return result_text


def update_error_counts(language, result_data):
    """Update error counts for given errors."""
    for error_data in result_data:
        error, created = Error.objects.get_or_create(language=language, code=error_data['error_code'])
        error.count = F('count') + 1
        error.save()
