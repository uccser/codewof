"""Module for the custom Django backdate_points_and_achievements command."""

from django.core.management.base import BaseCommand
from programming.codewof_utils import backdate_points_and_achievements


class Command(BaseCommand):
    """Required command class for the custom Django backdate command."""

    help = 'Loads questions into the database'

    def add_arguments(self, parser):
        """Interprets arguments passed to command."""
        parser.add_argument(
            '--ignore_flags',
            action='store_true',
            help='ignore status of backdate flags',
        )
        parser.add_argument(
            '--profiles',
            default=250,
            help='number of profiles to backdate',
        )

    def handle(self, *args, **options):
        """Automatically called when the backdate command is given."""
        print("Backdating points and achievements\n")
        ignore_flags = options['ignore_flags']
        number = int(options['profiles'])
        if ignore_flags and number > 0:
            raise ValueError("If ignoring backdate flags you must backdate all profiles.")
        backdate_points_and_achievements(number, ignore_flags)
