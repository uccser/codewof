"""Views for users application."""
import json
import logging

from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, DeleteView
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models.functions import Lower
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from users.serializers import (
    UserSerializer,
    UserTypeSerializer,
    GroupSerializer,
    MembershipSerializer,
    GroupRoleSerializer,
    InvitationSerializer,
    EmailReminderSerializer,
)
from users.forms import UserChangeForm, GroupCreateUpdateForm, GroupInvitationsForm
from functools import wraps
from allauth.account.admin import EmailAddress

from programming.models import (
    Attempt,
    Achievement
)
from users.models import (
    Group,
    Membership,
    GroupRole,
    Invitation,
    UserType,
    EmailReminder,
)
from programming.codewof_utils import get_questions_answered_in_past_month, backdate_user
from programming.question_recommendations import get_recommended_questions, get_recommendation_descriptions
from users.mixins import AdminRequiredMixin, AdminOrMemberRequiredMixin, SufficientAdminsMixin, \
    RequestUserIsMembershipUserMixin
from users.utils import send_invitation_email

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
        memberships = user.membership_set.all().order_by('group__name')
        groups = memberships.values('group').distinct()
        emails = EmailAddress.objects.annotate(email_lower=Lower('email')).filter(user=user, verified=True)
        invitations = Invitation.objects.filter(email__in=emails.values('email_lower')).exclude(group__in=groups)\
            .order_by('group__pk', '-date_sent').distinct('group__pk')

        context = super().get_context_data(**kwargs)
        recommendation_descriptions = get_recommendation_descriptions()
        recommended_questions = get_recommended_questions(user.profile)
        if len(recommendation_descriptions) == len(recommended_questions):
            context['recommendations'] = [(description, question) for description, question in zip(
                recommendation_descriptions, recommended_questions
            )]
        context['memberships'] = memberships
        context['invitations'] = invitations
        context['codewof_profile'] = self.object.profile
        context['goal'] = user.profile.goal
        context['all_achievements'] = Achievement.objects.all()
        questions_answered = get_questions_answered_in_past_month(user.profile)
        context['num_questions_answered'] = questions_answered
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


class UserTypeAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows user types to be viewed."""

    permission_classes = [IsAdminUser]
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer


class GroupCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new group."""

    model = Group
    form_class = GroupCreateUpdateForm

    def get_success_url(self):
        """URL to route to on successful update."""
        return reverse('users:dashboard')

    def form_valid(self, form):
        """Create a Membership between the creator user and the new Group."""
        response = super().form_valid(form)
        membership = Membership(user=self.request.user, group=form.instance, role=GroupRole.objects.get(name="Admin"))
        membership.save()
        return response


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
        group = self.get_object()
        context = super().get_context_data(**kwargs)
        admin_role = GroupRole.objects.get(name="Admin")

        user_membership = Membership.objects.all().get(user=user, group=group)
        context['is_admin'] = user_membership.role == admin_role
        context['user_membership'] = user_membership

        memberships = Membership.objects.filter(group=group).order_by('role__name', 'user__first_name',
                                                                      'user__last_name')
        context['memberships'] = memberships

        context['only_admin'] = False
        admins = context['memberships'].filter(role=admin_role)
        if len(admins) == 1 and admins[0] == user_membership:
            context['only_admin'] = True
        context['roles'] = GroupRole.objects.all()

        if group.feed_enabled:
            context['feed'] = Attempt.objects.filter(passed_tests=True, profile__user__in=memberships.values('user')
                                                     ).order_by('-datetime')[:10]

        return context


class GroupDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """View for deleting a group."""

    model = Group

    def get_success_url(self):
        """URL to route to on successful delete."""
        return reverse('users:dashboard')


def admin_required(f):
    """Check the user is an Admin of the Group decorator."""

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


def member_or_admin_required(f):
    """Check the user is a Member or Admin of the Group decorator."""

    @wraps(f)
    def g(request, *args, **kwargs):
        group = Group.objects.get(pk=kwargs['pk'])
        if Membership.objects.all().filter(user=request.user, group=group):
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
    """View for updating memberships from JSON."""
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
            sent = []
            skipped = []

            for email in emails:
                email = email.lower().strip()
                if len(Invitation.objects.filter(email=email, group=group)) > 0:
                    skipped.append(email)
                    continue

                try:
                    user = EmailAddress.objects.annotate(email_lower=Lower('email')).get(email_lower=email).user
                    invitee_emails = EmailAddress.objects.annotate(email_lower=Lower('email')).filter(user=user)
                except EmailAddress.DoesNotExist:
                    user = None

                # If user with that email exists and they are already a member or an invitation has been sent to one of
                # their other emails.
                if user is not None and (len(Membership.objects.filter(user=user, group=group)) > 0
                                         or len(Invitation.objects.filter(
                        email__in=invitee_emails.values('email_lower'), group=group)) > 0):
                    skipped.append(email)
                    continue

                Invitation(group=group, inviter=request.user, email=email).save()
                send_invitation_email(user, request.user, group.name, email)
                sent.append(email)

            build_messages(sent, skipped, request)
            return HttpResponseRedirect(reverse('users:groups-detail', args=[pk]))
    else:
        form = GroupInvitationsForm()

    return render(request, 'users/create_invitations.html', {'form': form})


def build_messages(sent, skipped, request):
    """
    Build a Django message to notify the user which invitation emails were successful.

    :param sent: A list of emails that invitations were sent to.
    :param skipped: A list of emails that were skipped.
    :param request: The request object.
    :return:
    """
    sent_message = "The following emails had invitations sent to them: "
    skipped_message = "The following emails were skipped either because they have already been invited or "\
                      "are already a member of the group: "
    for email in sent:
        sent_message += email + ", "
    for email in skipped:
        skipped_message += email + ", "

    if len(sent) > 0:
        messages.add_message(request, messages.SUCCESS, sent_message.rstrip(' ,'))
    if len(skipped) > 0:
        messages.add_message(request, messages.WARNING, skipped_message.rstrip(' ,'))


def invitee_required(f):
    """Check the user is the invitee of the Invitation decorator."""

    @wraps(f)
    def g(request, *args, **kwargs):
        emails = EmailAddress.objects.annotate(email_lower=Lower('email')).filter(user=request.user, verified=True)
        if Invitation.objects.filter(pk=kwargs['pk'], email__in=emails.values('email_lower')):
            return f(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    return g


@require_http_methods(["POST"])
@login_required()
@invitee_required
def accept_invitation(request, pk):
    """
    View for accepting an invitation and creating a membership.

    Removes any duplicate invitations as well.
    """
    invitation = Invitation.objects.get(pk=pk)
    membership_role = GroupRole.objects.get(name="Member")
    if not Membership.objects.filter(user=request.user, group=invitation.group).exists():
        Membership(user=request.user, group=invitation.group, role=membership_role).save()

    emails = EmailAddress.objects.annotate(email_lower=Lower('email')).filter(user=request.user)
    Invitation.objects.filter(email__in=emails.values('email_lower'), group=invitation.group).delete()

    return HttpResponse()


@require_http_methods(["DELETE"])
@login_required()
@invitee_required
def reject_invitation(request, pk):
    """
    View for rejecting an invitation.

    Removes any duplicate invitations as well.
    """
    invitation = Invitation.objects.get(pk=pk)
    emails = EmailAddress.objects.annotate(email_lower=Lower('email')).filter(user=request.user)
    Invitation.objects.filter(email__in=emails.values('email_lower'), group=invitation.group).delete()

    return HttpResponse()


@require_http_methods(["GET"])
@login_required()
@member_or_admin_required
def get_group_emails(request, pk, group):
    """View for obtaining the email addresses of the members of the group."""
    emails_list = list(group.users.values_list('email', flat=True))
    return JsonResponse({"emails": emails_list})


class GroupAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows groups to be viewed."""

    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MembershipAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows group memberships to be viewed."""

    permission_classes = [IsAdminUser]
    queryset = Membership.objects.all().select_related('user', 'group', 'role')
    serializer_class = MembershipSerializer


class GroupRoleAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows group roles to be viewed."""

    permission_classes = [IsAdminUser]
    queryset = GroupRole.objects.all()
    serializer_class = GroupRoleSerializer


class InvitationAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows group invitations to be viewed."""

    permission_classes = [IsAdminUser]
    queryset = Invitation.objects.all().select_related('group', 'inviter')
    serializer_class = InvitationSerializer


class EmailReminderAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows email reminders to be viewed."""

    permission_classes = [IsAdminUser]
    queryset = EmailReminder.objects.all().select_related('user')
    serializer_class = EmailReminderSerializer
