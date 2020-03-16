"""Utilities for the style checker application."""

from django.template.loader import render_to_string


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
