"""Mixins for user application views."""

from django.core.exceptions import PermissionDenied
from users.models import Membership, GroupRole


class AdminRequiredMixin:
    """Mixin for checking the user is an Admin of the Group."""

    def dispatch(self, request, *args, **kwargs):
        """Dispatch for AdminRequiredMixin."""
        admin_role = GroupRole.objects.get(name="Admin")
        if Membership.objects.all().filter(user=self.request.user, group=self.get_object(), role=admin_role):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class AdminOrMemberRequiredMixin:
    """Mixin for checking the user is an Admin or Member of the Group."""

    def dispatch(self, request, *args, **kwargs):
        """Dispatch for AdminOrMemberRequiredMixin."""
        if Membership.objects.all().filter(user=self.request.user, group=self.get_object()):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class SufficientAdminsMixin:
    """Mixin for checking there will be enough Admins if deleting an Admin Membership."""

    def dispatch(self, request, *args, **kwargs):
        """Dispatch for SufficientAdminsMixin."""
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
        """Dispatch for RequestUserIsMembershipUserMixin."""
        membership = self.get_object()
        if request.user == membership.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
