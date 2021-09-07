"""Module for the custom Django create_admin command."""

from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import UserType
from allauth.account.models import EmailAddress

LOG_HEADER = '\n{}\n' + ('-' * 20)


class Command(management.base.BaseCommand):
    """Required command class for the custom Django create_admin command."""

    help = "Create admin account."

    def handle(self, *args, **options):
        """Automatically called when the create_admin command is given."""
        User = get_user_model()  # noqa N806

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

        print('Admin account created.\n')
