"""Module for the custom Django backdate_points_and_badges command."""

from django.core.management.base import BaseCommand
from codewof.codewof_utils import backdate_points_and_badges


class Command(BaseCommand):
    """Required command class for the custom Django backdate command."""

    help = 'Loads questions into the database'

    def handle(self, *args, **options):
        """Automatically called when the backdate command is given."""
        backdate_points_and_badges()
