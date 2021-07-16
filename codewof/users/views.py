"""Views for users application."""
import json
import logging
from random import Random

from django.conf import settings as django_settings
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, DeleteView
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from users.serializers import UserSerializer
from programming import settings
from users.forms import UserChangeForm, GroupCreateUpdateForm, GroupInvitationsForm
from research.models import StudyRegistration
from functools import wraps
from allauth.account.admin import EmailAddress

from programming.models import (
    Question,
    Attempt,
    Achievement
)
from users.models import Group, Membership, GroupRole, Invitation

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

        user_membership = Membership.objects.all().get(user=user, group=self.get_object())
        context['is_admin'] = user_membership.role == admin_role
        context['user_membership'] = user_membership

        context['memberships'] = Membership.objects.filter(group=self.get_object()).order_by('role__name',
                                                                                             'user__first_name',
                                                                                             'user__last_name')
        context['only_admin'] = False
        admins = context['memberships'].filter(role=admin_role)
        if len(admins) == 1 and admins[0] == user_membership:
            context['only_admin'] = True
        context['roles'] = GroupRole.objects.all()
        return context


class GroupDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """View for deleting a group."""

    model = Group

    def get_success_url(self):
        """URL to route to on successful delete."""
        return reverse('users:dashboard')


def admin_required(f):
    """Decorator for checking the user is an Admin of the Group."""

    @wraps(f)
    def g(request, *args, **kwargs):
        admin_role = GroupRole.objects.get(name="Admin")
        group = Group.objects.get(pk=kwargs['pk'])
        if Membership.objects.all().filter(user=request.user, group=group, role=admin_role):
            kwargs['group'] = group
            return f(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    return g


@require_http_methods(["PUT"])
@login_required()
@admin_required
@transaction.atomic
def update_memberships(request, pk, group):
    """
    View for updating memberships from JSON.

    TODO: Replace Exception with a more descriptive Exception
    """
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    memberships = body['memberships']

    for membership in memberships:
        id = membership['id']
        delete = membership['delete']
        role = membership['role']

        if type(id) != int:
            raise Exception("One of the membership objects has an id that is not an integer (id={}).".format(id))
        if type(delete) != bool:
            raise Exception("One of the membership objects has delete value that is not a boolean (id={}).".format(id))

        membership_object = Membership.objects.filter(id=id)
        if len(membership_object) == 0:
            raise ObjectDoesNotExist
        else:
            membership_object = membership_object[0]

        if delete:
            membership_object.delete()
        else:
            role_object = GroupRole.objects.filter(name=role)
            if len(role_object) == 0:
                raise Exception("One of the membership objects has a non-existent role (id={}).".format(id))
            else:
                membership_object.role = role_object[0]
                membership_object.save()

    if len(Membership.objects.filter(group=group, role=GroupRole.objects.get(name='Admin'))) == 0:
        raise Exception("Must have at least one Admin in the group.")

    return HttpResponse()


class SufficientAdminsMixin:
    """Mixin for checking there will be enough Admins if deleting an Admin Membership."""

    def dispatch(self, request, *args, **kwargs):
        membership = self.get_object()
        admin_role = GroupRole.objects.get(name='Admin')
        if len(Membership.objects.all().filter(group=membership.group,
                                               role=admin_role)) > 1 or membership.role != admin_role:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Exception("A Group must have at least one Admin.")


class RequestUserIsMembershipUserMixin:
    """Mixin for checking the user making the request is the user of the Membership."""

    def dispatch(self, request, *args, **kwargs):
        membership = self.get_object()
        if request.user == membership.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class MembershipDeleteView(LoginRequiredMixin, RequestUserIsMembershipUserMixin, SufficientAdminsMixin, DeleteView):
    """View for deleting a membership."""

    model = Membership

    def get_success_url(self):
        """URL to route to on successful delete."""
        return reverse('users:dashboard')


@login_required()
@admin_required
def create_invitations(request, pk, group):
    """View for creating invitations to join a group and sending out emails."""

    if request.method == 'POST':
        form = GroupInvitationsForm(request.POST)
        if form.is_valid():
            emails = form.cleaned_data.get('emails').splitlines()

            for email in emails:
                try:
                    user = EmailAddress.objects.get(email=email).user
                except EmailAddress.DoesNotExist:
                    user = None

                Invitation(group=group, inviter=request.user, email=email).save()
                send_invitation_email(user, request.user, group.name, email)

            return HttpResponseRedirect(reverse('users:groups-detail', args=[pk]))
    else:
        form = GroupInvitationsForm()

    return render(request, 'users/create_invitations.html', {'form': form})


def send_invitation_email(invitee, inviter, group_name, email):
    """
    A function to handle sending an invitation email.
    :param invitee: The User receiving the invite, which is null if the User does not exist yet.
    :param inviter: The User creating the invite.
    :param group_name: The name of the Group to be joined.
    :param email: The invitee's email address.
    :return:
    """
    if invitee is None:
        html = create_invitation_html(False, None, inviter.first_name + " " + inviter.last_name, group_name, email)
        plain = create_invitation_plaintext(False, None, inviter.first_name + " " + inviter.last_name, group_name, email)
    else:
        html = create_invitation_html(True, invitee.first_name, inviter.first_name + " " + inviter.last_name,
                                      group_name, email)
        plain = create_invitation_plaintext(True, invitee.first_name, inviter.first_name + " " + inviter.last_name,
                                            group_name, email)

    send_mail(
        'CodeWOF Invitation',
        plain,
        django_settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
        html_message=html
    )


def create_invitation_plaintext(user_exists, invitee_name, inviter_name, group_name, email):
    """
    Builds the plaintext for the invitation email, which is different depending if an account with the email exists or
    not.
    :param user_exists: Whether a User object with this email exists.
    :param invitee_name: The name of the invitee.
    :param inviter_name: The name of the inviter.
    :param group_name: The name of the group.
    :param email: The email address.
    :return:
    """
    if user_exists:
        plaintext = "Hi {},\n\n{} has invited you to join the Group '{}'. Click the link below to sign in. You will " \
                    "see your invitation in the dashboard, where you can join the group.\n\n{}\n\nThanks,\nThe " \
                    "Computer Science Education Research Group".format(invitee_name, inviter_name, group_name,
                                                                       reverse('account_login'))
    else:
        plaintext = "Hi,\n\n{} has invited you to join the Group '{}'. CodeWOF helps you maintain your " \
                    "programming fitness with short daily programming exercises. With a free account you can save your " \
                    "progress and track your programming fitness over time. Click the link below to make an account," \
                    " using the email {}. You will see your invitation in the dashboard, where you can join the group. " \
                    "If you already have a CodeWOF account, then add {} to your profile to make the invitation appear." \
                    "\n\n{}\n\nThanks,\nThe Computer Science Education Research Group".format(inviter_name, group_name,
                                                                                              email, email,
                                                                                              reverse('account_signup'))
    return plaintext


def create_invitation_html(user_exists, invitee_name, inviter_name, group_name, email):
    """
    Builds the html for the invitation email, which is different depending if an account with the email exists or not.
    :param user_exists: Whether a User object with this email exists.
    :param invitee_name: The name of the invitee.
    :param inviter_name: The name of the inviter.
    :param group_name: The name of the group.
    :param email: The email address.
    :return:
    """
    email_template = get_template("users/group_invitation.html")
    if user_exists:
        message = "{} has invited you to join the Group '{}'. Click the button below to sign in. You will " \
                  "see your invitation in the dashboard, where you can join the group.".format(inviter_name, group_name)
        html = email_template.render({"user_exists": user_exists, "invitee_name": invitee_name, "message": message,
                                      "url": reverse('account_login'), "button_text": "Sign In"})
    else:
        message = "{} has invited you to join the Group '{}'. CodeWOF helps you maintain your " \
                  "programming fitness with short daily programming exercises. With a free account you can save your " \
                  "progress and track your programming fitness over time. Click the link below to make an account," \
                  " using the email {}. You will see your invitation in the dashboard, where you can join the group. " \
                  "If you already have a CodeWOF account, then add {} to your profile to make the invitation appear." \
            .format(inviter_name, group_name, email, email)
        html = email_template.render({"user_exists": user_exists, "invitee_name": invitee_name, "message": message,
                                      "url": reverse('account_signup'), "button_text": "Sign Up"})
    return html
