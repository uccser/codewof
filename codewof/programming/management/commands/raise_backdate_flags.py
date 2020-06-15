"""Module for the custom Django raise_backdate_flags command."""

from django.core.management.base import BaseCommand
from programming.models import Profile


class Command(BaseCommand):
    """Required command class for the custom Django raise backdate flags command."""

    help = 'Raise flags for all user profiles, requiring them to be backdated'

    def handle(self, *args, **options):
        """Automatically called when the raise_backdate_flags command is given."""
        print("Raising backdate flags")
        profiles = Profile.objects.all()
        for profile in profiles:
            profile.has_backdated = False
            profile.full_clean()
            profile.save()
        print("Completed raising backdate flags\n")
