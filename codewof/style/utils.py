"""Utilities for the style checker application."""

from django.conf import settings
from django.db.models import F
from django.template.loader import render_to_string
from style.models import Error


CHARACTER_DESCRIPTIONS = {
    '(': 'opening bracket',
    ')': 'closing bracket',
    '[': 'opening square bracket',
    ']': 'closing square bracket',
    '{': 'opening curly bracket',
    '}': 'closing curly bracket',
    "'": 'single quote',
    '"': 'double quote',
    ':': 'colon',
    ';': 'semicolon',
    ' ': 'space',
    ',': 'comma',
    '.': 'full stop',
}


def get_language_slugs():
    """Return all programming language slugs.

    Returns:
        Iteratable of programming language slugs.
    """
    return settings.STYLE_CHECKER_LANGUAGES.keys()


def get_language_info(slug):
    """Return information about a programming language.

    Args:
        slug (str): The slug of the given language.

    Returns:
        Dictionary of information about the given programming language.
    """
    return settings.STYLE_CHECKER_LANGUAGES.get(slug, dict())


def get_article(word):
    """Return English article for word.

    Returns 'an' if word starts with vowel. Technically
    it should check the word sound, compared to the
    letter but this shouldn't occur with our words.

    Args:
        word (str): Word to create article for.

    Returns:
        'a' or 'an' (str) depending if word starts with vowel.
    """
    if word[0].lower() in 'aeiou':
        return 'an'
    else:
        return 'a'


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
