"""Context processor for checking if research is active."""

from research.settings import RESEARCH_ACTIVE


def research(request):
    """Return a dictionary containing booleans regarding environment.

    Returns:
        Dictionary containing deployed research boolean to add to context.
    """
    return {
        "RESEARCH": RESEARCH_ACTIVE,
    }
