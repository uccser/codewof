"""Context processor for booleans relating to deployed environment."""

from django.conf import settings


def deployed(request):
    """Return a dictionary containing booleans relating to deployed environment.

    Args:
        request (Request): The HTTP request.

    Returns:
        Dictionary containing booleans relating to deployed environment.
    """
    return {
        "DEPLOYED": settings.DJANGO_PRODUCTION,
        "DEPLOYMENT_TYPE": settings.DEPLOYMENT_TYPE,
    }
