from django.core.management import BaseCommand
from django.utils import timezone

from users.models import Invitation


class Command(BaseCommand):
    """Required command class for the custom Django removed_expired_invitations command."""

    def handle(self, *args, **options):
        """Gets Invitations that have expired and deletes them."""
        today = timezone.now()
        Invitation.objects.filter(date_expires__lte=today).delete()
