"""Module for the custom Django sampledata command."""

from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import UserType
from allauth.account.models import EmailAddress
from tests.users.factories import UserFactory
from tests.research.factories import (
    StudyFactory,
    StudyGroupFactory,
)

from codewof.models import Badge, Attempt

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

        management.call_command('load_user_types')
        print(LOG_HEADER.format('Create sample users'))
        User = get_user_model()
        # Create admin account
        admin = User.objects.create_superuser(
            'admin',
            'admin@codewof.co.nz',
            password=settings.SAMPLE_DATA_ADMIN_PASSWORD,
            first_name='Admin',
            last_name='Account',
            user_type=UserType.objects.get(slug='teacher')
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
            last_name='Doe',
            user_type=UserType.objects.get(slug='student')
        )
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=True
        )
        UserFactory.create_batch(size=100)
        print('Users created.')

        # Codewof
        management.call_command('load_questions')
        print('Programming questions loaded.')

        # Research
        StudyFactory.create_batch(size=5)
        StudyGroupFactory.create_batch(size=15)
        print('Research studies loaded.')

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

        Badge.objects.create(
            id_name='consecutive-days-2',
            display_name='Worked on coding for two days in a row!',
            description='Attempted at least one question two days in a row',
            icon_name='img/icons/badges/icons8-calendar-2-50.png'
        )

        Badge.objects.create(
            id_name='consecutive-days-7',
            display_name='Worked on coding every day for one week!',
            description='Attempted at least one question every day for one week',
            icon_name='img/icons/badges/icons8-calendar-7-50.png'
        )

        Badge.objects.create(
            id_name='consecutive-days-14',
            display_name='Worked on coding every day for two weeks!',
            description='Attempted at least one question every day for two weeks',
            icon_name='img/icons/badges/icons8-calendar-14-50.png'
        )

        Badge.objects.create(
            id_name='consecutive-days-21',
            display_name='Worked on coding every day for three weeks!',
            description='Attempted at least one question every day for three weeks',
            icon_name='img/icons/badges/icons8-calendar-21-50.png'
        )

        Badge.objects.create(
            id_name='consecutive-days-28',
            display_name='Worked on coding every day for four weeks!',
            description='Attempted at least one question every day for four weeks',
            icon_name='img/icons/badges/icons8-calendar-28-50.png'
        )


        print("Badges added.")
