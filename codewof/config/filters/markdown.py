"""Template filter for rendering Markdown to HTML."""

from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from markdownx.utils import markdownify

register = template.Library()


@register.filter
@stringfilter
def markdown(raw_markdown):
    """Render Markdown as HTML.

    Args:
        raw_markdown (str): Text of raw Markdown.

    Returns:
        HTML string of rendered Markdown marked as safe.
    """
    return mark_safe(markdownify(raw_markdown))
