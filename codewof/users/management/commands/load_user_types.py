"""Module for the custom Django load_user_types command."""

from django.core.management.base import BaseCommand
from users.models import UserType
from django.utils.translation import gettext as _

USER_TYPES = [
    {
        'slug': 'student',
        'name': _('Student'),
    },
    {
        'slug': 'teacher',
        'name': _('Teacher'),
    },
    {
        'slug': 'other',
        'name': _('Other'),
    },
]


class Command(BaseCommand):
    """Required command class for the custom Django load_user_types command."""

    help = 'Loads user types into the database'

    def handle(self, *args, **options):
        """Automatically called when the load_user_types command is given."""
        for order_number, user_type_data in enumerate(USER_TYPES):
            slug = user_type_data.pop('slug')
            user_type_data['order'] = order_number
            user_type, created = UserType.objects.update_or_create(
                slug=slug,
                defaults=user_type_data,
            )

            # Print logging message
            if created:
                verb_text = 'Added'
            else:
                verb_text = 'Updated'
            print('{} user group: {}'.format(verb_text, user_type_data['name']))
