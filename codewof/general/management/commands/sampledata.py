"""Module for the custom Django sampledata command."""

import csv
import random
from django.core import management
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from allauth.account.models import EmailAddress
from codewof.models import (
    QuestionTypeProgram,
    QuestionTypeProgramTestCase,
    QuestionTypeFunction,
    QuestionTypeFunctionTestCase,
    QuestionTypeParsons,
    QuestionTypeParsonsTestCase,
)


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
