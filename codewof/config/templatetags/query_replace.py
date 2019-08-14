"""Module for the custom query_replace template tag."""

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def query_replace(context, **kwargs):
    """Render URL query string with given values replaced.

    Args:
        context (dict): Dictionary of view context.

    Returns:
        Rendered query string.
    """
    querydict = context['request'].GET.copy()
    for key, value in kwargs.items():
        querydict[key] = value
    return querydict.urlencode()
