"""Views for users application."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView


from codewof.models import (
    Profile,
    Question,
    TestCase,
    Attempt,
    TestCaseAttempt,
    Badge,
    Earned
)

from codewof.codewof_utils import check_badge_conditions, get_past_5_weeks, add_points

import logging

User = get_user_model()

logger = logging.getLogger(__name__)
del logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'incremental': True,
    'root': {
        'level': 'DEBUG',
    },
}


class UserDetailView(LoginRequiredMixin, DetailView):
    """View for a user's profile."""

    model = User
    context_object_name = 'user'

    def get_object(self):
        """Get object for template."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['codewof_profile'] = self.object.profile
        context['goal'] = user.profile.goal
        context['all_badges'] = Badge.objects.all()
        check_badge_conditions(user)
        context["a"] = "b"
        context['past_5_weeks'] = get_past_5_weeks(user)
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating user data."""

    model = User
    fields = ['first_name', 'last_name']

    def get_success_url(self):
        """URL to route to on successful update."""
        return reverse('users:profile')

    def get_object(self):
        """Object to perform update with."""
        return User.objects.get(pk=self.request.user.pk)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """View for redirecting to a user's webpage."""

    permanent = False

    def get_redirect_url(self):
        """URL to redirect to."""
        return reverse("users:profile")
