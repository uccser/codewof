"""Views for users application."""

import logging
from random import Random

from django.http import HttpResponseForbidden
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, DeleteView
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from users.serializers import UserSerializer
from programming import settings
from users.forms import UserChangeForm, GroupCreateUpdateForm
from research.models import StudyRegistration


from programming.models import (
    Question,
    Attempt,
    Achievement
)
from users.models import Group, Membership, GroupRole

from programming.codewof_utils import get_questions_answered_in_past_month, backdate_user

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
    """View for a user's dashboard."""

    model = User
    context_object_name = 'user'
    template_name = 'users/dashboard.html'

    def get_object(self):
        """Get object for template."""
        user = self.request.user
        if not user.profile.has_backdated:
            backdate_user(user.profile)
        return user

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        user = self.request.user
        if not user.profile.has_backdated:
            backdate_user(user.profile)
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        today = now.date()

        if user.is_authenticated:
            # Look for active study registration
            try:
                study_registration = StudyRegistration.objects.get(
                    user=user,
                    study_group__study__start_date__lte=now,
                    study_group__study__end_date__gte=now,
                )
            except ObjectDoesNotExist:
                study_registration = None

        # Get questions not attempted before today
        if study_registration:
            questions = study_registration.study_group.questions.all()
        else:
            questions = Question.objects.all()

        log_message = 'Questions for user {} on {} ({}):\n'.format(user, now, today)
        for i, question in enumerate(questions):
            log_message += '{}: {}\n'.format(i, question)
        logger.info(log_message)

        # TODO: Also filter by questions added before today
        questions = questions.filter(
            Q(attempt__isnull=True)
            | (Q(attempt__passed_tests=False) & Q(attempt__datetime__date__lte=today))
            | (Q(attempt__passed_tests=True) & Q(attempt__datetime__date=today))
        ).order_by('pk').distinct('pk').select_subclasses()
        questions = list(questions)

        log_message = 'Filtered questions for user {}:\n'.format(user)
        for i, question in enumerate(questions):
            log_message += '{}: {}\n'.format(i, question)
        logger.info(log_message)

        # Randomly pick 3 based off seed of todays date
        if len(questions) > 0:
            random_seeded = Random('{}{}'.format(user.pk, today))
            number_to_do = min(len(questions), settings.QUESTIONS_PER_DAY)
            todays_questions = random_seeded.sample(questions, number_to_do)
            all_complete = True
            for question in todays_questions:
                question.completed = Attempt.objects.filter(
                    profile=user.profile,
                    question=question,
                    passed_tests=True,
                ).exists()
                if all_complete and not question.completed:
                    all_complete = False
        else:
            todays_questions = list()
            all_complete = False

        log_message = 'Chosen questions for user {}:\n'.format(user)
        for i, question in enumerate(todays_questions):
            log_message += '{}: {}\n'.format(i, question)
        logger.info(log_message)

        context['questions_to_do'] = todays_questions
        context['all_complete'] = all_complete

        # Show studies
        studies = user.user_type.studies.filter(
            visible=True,
            groups__isnull=False,
        ).distinct()
        memberships = user.membership_set.all().order_by('group__name')

        # TODO: Simplify to one database query
        for study in studies:
            study.registered = StudyRegistration.objects.filter(
                user=user,
                study_group__in=study.groups.all(),
            ).exists()
        context['studies'] = studies
        context['memberships'] = memberships
        context['codewof_profile'] = self.object.profile
        context['goal'] = user.profile.goal
        context['all_achievements'] = Achievement.objects.all()
        questions_answered = get_questions_answered_in_past_month(user.profile)
        context['num_questions_answered'] = questions_answered
        logger.debug(questions_answered)
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating user data."""

    model = User
    form_class = UserChangeForm

    def get_success_url(self):
        """URL to route to on successful update."""
        return reverse('users:dashboard')

    def get_object(self):
        """Object to perform update with."""
        return User.objects.get(pk=self.request.user.pk)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """View for redirecting to a user's webpage."""

    permanent = False

    def get_redirect_url(self):
        """URL to redirect to."""
        return reverse("users:dashboard")


class UserAchievementsView(LoginRequiredMixin, DetailView):
    """View for a user's achievements."""

    model = User
    context_object_name = 'user'
    template_name = 'users/achievements.html'

    def get_object(self):
        """Get object for template."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['achievements_not_earned'] = Achievement.objects.all().difference(
            user.profile.earned_achievements.all()
        )
        context['num_achievements_earned'] = user.profile.earned_achievements.all().count()
        context['num_achievements'] = Achievement.objects.all().count()
        return context


class UserAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows users to be viewed."""

    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new group."""

    model = Group
    form_class = GroupCreateUpdateForm

    def get_success_url(self):
        """URL to route to on successful update."""
        return reverse('users:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        membership = Membership(user=self.request.user, group=form.instance, role=GroupRole.objects.get(name="Admin"))
        membership.save()
        return response


class AdminRequiredMixin:
    """Mixin for checking the user is an Admin of the Group."""

    def dispatch(self, request, *args, **kwargs):
        admin_role = GroupRole.objects.get(name="Admin")
        if Membership.objects.all().filter(user=self.request.user, group=self.get_object(), role=admin_role):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class AdminOrMemberRequiredMixin:
    """Mixin for checking the user is an Admin or Member of the Group."""

    def dispatch(self, request, *args, **kwargs):
        if Membership.objects.all().filter(user=self.request.user, group=self.get_object()):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class GroupUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """View for updating a group."""

    model = Group
    form_class = GroupCreateUpdateForm

    def get_success_url(self):
        """URL to route to on successful update."""
        return reverse('users:groups-detail', args=[self.get_object().pk])


class GroupDetailView(LoginRequiredMixin, AdminOrMemberRequiredMixin, DetailView):
    """View for viewing the details of a group."""

    model = Group

    def get_context_data(self, **kwargs):
        """Get additional context data for template."""
        user = self.request.user
        context = super().get_context_data(**kwargs)
        admin_role = GroupRole.objects.get(name="Admin")
        context['is_admin'] = len(Membership.objects.all().filter(user=user, group=self.get_object(),
                                                                  role=admin_role)) != 0
        return context


class GroupDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """View for deleting a group."""

    model = Group

    def get_success_url(self):
        """URL to route to on successful delete."""
        return reverse('users:dashboard')
