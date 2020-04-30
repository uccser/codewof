"""Module for the custom Django load_badges command."""

from django.core.management.base import BaseCommand
from programming.models import Badge

# TODO: Relocate
BADGES = [
    {
        'id_name':      'create-account',
        'display_name': 'Created an account!',
        'description':  'Created your very own account',
        'icon_name':    'img/icons/badges/icons8-badge-create-account-48.png',
        'badge_tier':   0,
        'parent':       None
    },
    {
        'id_name':      'questions-solved-100',
        'display_name': 'Solved one hundred questions!',
        'description':  'Solved one hundred questions',
        'icon_name':    'img/icons/badges/icons8-question-solved-gold-50.png',
        'badge_tier':   4,
        'parent':       None
    },
    {
        'id_name':      'questions-solved-10',
        'display_name': 'Solved ten questions!',
        'description':  'Solved ten questions',
        'icon_name':    'img/icons/badges/icons8-question-solved-silver-50.png',
        'badge_tier':   3,
        'parent':       'questions-solved-100'
    },
    {
        'id_name':      'questions-solved-5',
        'display_name': 'Solved five questions!',
        'description':  'Solved five questions',
        'icon_name':    'img/icons/badges/icons8-question-solved-bronze-50.png',
        'badge_tier':   2,
        'parent':       'questions-solved-10'
    },
    {
        'id_name':      'questions-solved-1',
        'display_name': 'Solved one question!',
        'description':  'Solved your very first question',
        'icon_name':    'img/icons/badges/icons8-question-solved-black-50.png',
        'badge_tier':   1,
        'parent':       'questions-solved-5'
    },
    {
        'id_name':      'attempts-made-100',
        'display_name': 'Made one hundred question attempts!',
        'description':  'Attempted one hundred questions',
        'icon_name':    'img/icons/badges/icons8-attempt-made-gold-50.png',
        'badge_tier':   4,
        'parent':       None
    },
    {
        'id_name':      'attempts-made-10',
        'display_name': 'Made ten question attempts!',
        'description':  'Attempted ten questions',
        'icon_name':    'img/icons/badges/icons8-attempt-made-silver-50.png',
        'badge_tier':   3,
        'parent':       'attempts-made-100'
    },
    {
        'id_name':      'attempts-made-5',
        'display_name': 'Made five question attempts!',
        'description':  'Attempted five questions',
        'icon_name':    'img/icons/badges/icons8-attempt-made-bronze-50.png',
        'badge_tier':   2,
        'parent':       'attempts-made-10'
    },
    {
        'id_name':      'attempts-made-1',
        'display_name': 'Made your first question attempt!',
        'description':  'Attempted one question',
        'icon_name':    'img/icons/badges/icons8-attempt-made-black-50.png',
        'badge_tier':   1,
        'parent':       'attempts-made-5'
    },
    {
        'id_name':      'consecutive-days-28',
        'display_name': 'Worked on coding every day for four weeks!',
        'description':  'Attempted at least one question every day for four weeks',
        'icon_name':    'img/icons/badges/icons8-calendar-28-50.png',
        'badge_tier':   5,
        'parent':       None
    },
    {
        'id_name':      'consecutive-days-21',
        'display_name': 'Worked on coding every day for three weeks!',
        'description':  'Attempted at least one question every day for three weeks',
        'icon_name':    'img/icons/badges/icons8-calendar-21-50.png',
        'badge_tier':   4,
        'parent':       'consecutive-days-28'
    },
    {
        'id_name':      'consecutive-days-14',
        'display_name': 'Worked on coding every day for two weeks!',
        'description':  'Attempted at least one question every day for two weeks',
        'icon_name':    'img/icons/badges/icons8-calendar-14-50.png',
        'badge_tier':   3,
        'parent':       'consecutive-days-21'
    },
    {
        'id_name':      'consecutive-days-7',
        'display_name': 'Worked on coding every day for one week!',
        'description':  'Attempted at least one question every day for one week',
        'icon_name':    'img/icons/badges/icons8-calendar-7-50.png',
        'badge_tier':   2,
        'parent':       'consecutive-days-14'
    },
    {
        'id_name':      'consecutive-days-2',
        'display_name': 'Worked on coding for two days in a row!',
        'description':  'Attempted at least one question two days in a row',
        'icon_name':    'img/icons/badges/icons8-calendar-2-50.png',
        'badge_tier':   1,
        'parent':       'consecutive-days-7'
    },
]


class Command(BaseCommand):
    """Required command class for the custom Django load_badges command.

    Future plan: Create full loader like the load_questions command
    """

    help = 'Loads badges into the database'

    def handle(self, *args, **options):
        """Automatically called when the load_badges command is given."""
        all_badges = {}

        for badge in BADGES:
            all_badges[badge['id_name']], created = Badge.objects.update_or_create(
                id_name=badge['id_name'],
                defaults={
                    'display_name': badge['display_name'],
                    'description': badge['description'],
                    'icon_name': badge['icon_name'],
                    'badge_tier': badge['badge_tier'],
                    'parent': None if badge['parent'] is None else all_badges[badge['parent']]
                }
            )
            print("{} badge: {}".format("Created" if created else "Updated", badge['id_name']))

        print("{} badges loaded!\n".format(len(all_badges)))
