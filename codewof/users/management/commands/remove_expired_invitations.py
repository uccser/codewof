"""Module for the custom Django remove_expired_invitations command."""

from django.core.management import BaseCommand
from django.utils import timezone

from users.models import Invitation


class Command(BaseCommand):
    """Required command class for the custom Django removed_expired_invitations command."""

    def handle(self, *args, **options):
        """Get Invitations that have expired and delete them."""
        today = timezone.now()
        Invitation.objects.filter(date_expires__lte=today).delete()
