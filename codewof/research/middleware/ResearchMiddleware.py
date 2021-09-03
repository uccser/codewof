"""Middleware for research application."""

from django.utils.timezone import now
from django.conf import settings
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import (
    MiddlewareNotUsed,
    PermissionDenied,
    ObjectDoesNotExist,
)
from research.settings import (
    RESEARCH_ACTIVE,
    START_DATETIME,
    END_DATETIME,
    USER_TYPES_ALLOWED,
)
from research.models import StudyRegistration

# Wide net for allowing URLs
# django-allauth account URLs are not namespaced so checked manually.
ALLOWED_URL_NAMESPACES = [
    'admin',
    'research'
]
# Specific URLs to be allowed
ALLOWED_URL_PATHS = [
    '/',
    '/contact-us/',
    '/faq/',
    '/policies/',
]


class ResearchMiddleware:
    """Middleware used with research application."""

    def __init__(self, get_response):
        """One-time configuration and initialization.

        Only load research middleware if running in a staging enviroment.
        """
        if not settings.PRODUCTION_ENVIRONMENT:
            self.get_response = get_response
        else:
            raise MiddlewareNotUsed()

    def __call__(self, request):
        """Logic for middleware."""
        try:
            if RESEARCH_ACTIVE:
                self.process_request(request)
        except LoginRequired:
            messages.warning(
                request,
                'You need to be logged in to access this page on the test website.'
            )
            redirect_url = reverse('account_login') + f'?next={request.path}'
            response = redirect(redirect_url)
        except NoStudyRegistration:
            messages.error(
                request,
                'You need to register for the research project to access this page on the test website.'
            )
            response = redirect('research:home')
        except UserTypeNotAllowed:
            messages.error(
                request,
                "We're sorry but you're not eligible for the current research study."
            )
            response = redirect('general:home')
        except StudyClosed:
            messages.error(
                request,
                "The study is not currently open, check the dates and times below."
            )
            response = redirect('research:home')
        else:
            response = self.get_response(request)
        return response

    def process_request(self, request):
        """Check request and either permits, redirects, or rejects request."""
        # Staff can always access all pages
        if request.user.is_staff:
            return request

        # Check if allowed URL
        if request.path in ALLOWED_URL_PATHS:
            return request
        elif resolve(request.path).namespace in ALLOWED_URL_NAMESPACES:
            return request
        elif request.path.startswith('/accounts/'):
            return request

        # Check if authenicated, otherwise redirect.
        if not request.user.is_authenticated:
            raise LoginRequired()

        if request.user.user_type.slug not in USER_TYPES_ALLOWED:
            raise UserTypeNotAllowed()

        # Check if consented, otherwise redirect.
        try:
            StudyRegistration.objects.get(user=request.user)
        except ObjectDoesNotExist:
            raise NoStudyRegistration()

        # Check if permitted for early access
        if request.user.has_perm('research.research_early_access'):
            return request

        # Check date, otherwise redirect.
        if START_DATETIME <= now() <= END_DATETIME:
            return request
        else:
            raise StudyClosed()


# Custom exceptions

class LoginRequired(PermissionDenied):
    """Exception if user is not logged in."""

    pass


class NoStudyRegistration(PermissionDenied):
    """Exception if user is not registered for study."""

    pass


class UserTypeNotAllowed(PermissionDenied):
    """Exception if user's type is not elgible for study."""

    pass


class StudyClosed(PermissionDenied):
    """Exception if study is not currently open."""

    pass
