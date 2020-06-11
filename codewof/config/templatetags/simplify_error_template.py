"""Module for the custom simplify_error_template template tag."""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

SEARCH_TEXT = '{article} {character_description}'
REPLACE_TEXT = 'a {character}'


@register.simple_tag
def simplify_error_template(template):
    """Simplify template for rendering to user.

    Args:
        template (str): String of template.

    Returns:
        Updated string.
    """
    new_text = template.replace(SEARCH_TEXT, REPLACE_TEXT)
    return mark_safe(new_text)
