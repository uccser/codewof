"""Module for the custom Django update_data command."""

from django.core import management


class Command(management.base.BaseCommand):
    """Required command class for the custom Django update_data command."""

    help = "Update data in database."

    def add_arguments(self, parser):
        """Interprets arguments passed to command."""
        parser.add_argument(
            '--skip_backdate',
            action='store_true',
            help='skip backdate step',
        )

    def handle(self, *args, **options):
        """Automatically called when the sampledata command is given."""
        skip = options['skip_backdate']

        management.call_command('load_user_types')
        print('User types loaded.\n')

        management.call_command('load_questions')
        print('Programming questions loaded.\n')

        management.call_command('load_achievements')
        print('Achievements loaded.\n')

        management.call_command('load_style_errors')
        print('Style errors loaded.\n')

        management.call_command('load_group_roles')
        print('Group roles loaded.\n')

        # Award points and achievements
        if not skip:
            management.call_command('backdate_points_and_achievements')
        else:
            print('Ignoring backdate step as requested.\n')
