"""Module for the custom Django load_user_types command."""

from copy import deepcopy
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from users.models import GroupRole

GROUP_ROLES = [
    {
        'slug': 'member',
        'name': _('Member'),
    },
    {
        'slug': 'admin',
        'name': _('Admin'),
    },
]


class Command(BaseCommand):
    """Required command class for the custom Django load_group_roles command."""

    help = 'Loads group roles into the database'

    def handle(self, *args, **options):
        """Automatically called when the load_group_roles command is given."""
        for order_number, group_role_data in enumerate(deepcopy(GROUP_ROLES)):
            slug = group_role_data.pop('slug')
            group_role_data['order'] = order_number
            group_role, created = GroupRole.objects.update_or_create(
                slug=slug,
                defaults=group_role_data,
            )

            # Print logging message
            if created:
                verb_text = 'Added'
            else:
                verb_text = 'Updated'
            print('{} group role: {}'.format(verb_text, group_role_data['name']))
