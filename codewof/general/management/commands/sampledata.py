"""Module for the custom Django sampledata command."""

from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

from codewof.models import Badge

LOG_HEADER = '\n{}\n' + ('-' * 20)


class Command(management.base.BaseCommand):
    """Required command class for the custom Django sampledata command."""

    help = "Add sample data to database."

    def handle(self, *args, **options):
        """Automatically called when the sampledata command is given."""
        if settings.DEPLOYMENT_TYPE == 'prod' and not settings.DEBUG:
            raise management.base.CommandError(
                'This command can only be executed in DEBUG mode on non-production website.'
            )

        # Clear all data
        print(LOG_HEADER.format('Wipe database'))
        management.call_command('flush', interactive=False)
        print('Database wiped.')

        print(LOG_HEADER.format('Create sample users'))
        User = get_user_model()
        # Create admin account
        admin = User.objects.create_superuser(
            'admin',
            'admin@codewof.co.nz',
            password=settings.SAMPLE_DATA_ADMIN_PASSWORD,
            first_name='Admin',
            last_name='Account'
        )
        EmailAddress.objects.create(
            user=admin,
            email=admin.email,
            primary=True,
            verified=True
        )
        print('Admin created.')

        # Create user account
        user = User.objects.create_user(
            'user',
            'user@codewof.co.nz',
            password=settings.SAMPLE_DATA_USER_PASSWORD,
            first_name='Alex',
            last_name='Doe'
        )
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=True
        )
        print('User created.')

        # Codewof
        management.call_command('load_questions')
        print('Programming question added.')

        Badge.objects.create(
            id_name='create-account',
            display_name='Created an account!',
            description='Created your very own account',
            icon_name='img/icons/badges/icons8-badge-create-account-48.png'
        )

        Badge.objects.create(
            id_name='questions-solved-1',
            display_name='Solved one question!',
            description='Solved your very first question',
            icon_name='img/icons/badges/icons8-question-solved-black-50.png'
        )

        Badge.objects.create(
            id_name='questions-solved-5',
            display_name='Solved five questions!',
            description='Solved five questions',
            icon_name='img/icons/badges/icons8-question-solved-bronze-50.png'
        )

        Badge.objects.create(
            id_name='questions-solved-10',
            display_name='Solved ten questions!',
            description='Solved ten questions',
            icon_name='img/icons/badges/icons8-question-solved-silver-50.png'
        )

        Badge.objects.create(
            id_name='questions-solved-100',
            display_name='Solved one hundred questions!',
            description='Solved one hundred questions',
            icon_name='img/icons/badges/icons8-question-solved-silver-50.png'
        )

        Badge.objects.create(
            id_name='attempts-made-1',
            display_name='Made your first attempt at a question!',
            description='Attempted one question',
            icon_name='img/icons/badges/icons8-attempt-made-black-50.png'
        )

        Badge.objects.create(
            id_name='attempts-made-5',
            display_name='Made five question attempts!',
            description='Attempted five questions',
            icon_name='img/icons/badges/icons8-attempt-made-bronze-50.png'
        )

        Badge.objects.create(
            id_name='attempts-made-10',
            display_name='Made ten question attempts!',
            description='Attempted ten questions',
            icon_name='img/icons/badges/icons8-attempt-made-silver-50.png'
        )

        Badge.objects.create(
            id_name='attempts-made-100',
            display_name='Made one hundred question attempts!',
            description='Attempted one hundred questions',
            icon_name='img/icons/badges/icons8-attempt-made-gold-50.png'
        )
        print("Badges added.")
