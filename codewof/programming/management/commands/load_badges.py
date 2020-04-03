"""Module for the custom Django load_badges command."""

from django.core.management.base import BaseCommand
from django.conf import settings
from utils.LoaderFactory import LoaderFactory
from programming.models import Badge


class Command(BaseCommand):
    """Required command class for the custom Django load_badges command.
    
    Future plan: Create full loader like the load_questions command"""

    help = 'Loads badges into the database'

    def handle(self, *args, **options):
        """Automatically called when the load_badges command is given."""
        createdAccount = Badge.objects.create(
            id_name='create-account',
            display_name='Created an account!',
            description='Created your very own account',
            icon_name='img/icons/badges/icons8-badge-create-account-48.png',
            badge_tier=0
        )
        print("Loaded badge: " + createdAccount.id_name)

        questionSolved100 = Badge.objects.create(
            id_name='questions-solved-100',
            display_name='Solved one hundred questions!',
            description='Solved one hundred questions',
            icon_name='img/icons/badges/icons8-question-solved-silver-50.png',
            badge_tier=4
        )
        print("Loaded badge: " + questionSolved100.id_name)

        questionSolved10 = Badge.objects.create(
            id_name='questions-solved-10',
            display_name='Solved ten questions!',
            description='Solved ten questions',
            icon_name='img/icons/badges/icons8-question-solved-silver-50.png',
            badge_tier=3,
            parent=questionSolved100
        )
        print("Loaded badge: " + questionSolved10.id_name)

        questionSolved5 = Badge.objects.create(
            id_name='questions-solved-5',
            display_name='Solved five questions!',
            description='Solved five questions',
            icon_name='img/icons/badges/icons8-question-solved-bronze-50.png',
            badge_tier=2,
            parent=questionSolved10
        )
        print("Loaded badge: " + questionSolved5.id_name)

        questionSolved1 = Badge.objects.create(
            id_name='questions-solved-1',
            display_name='Solved one question!',
            description='Solved your very first question',
            icon_name='img/icons/badges/icons8-question-solved-black-50.png',
            badge_tier=1,
            parent=questionSolved5
        )
        print("Loaded badge: " + questionSolved1.id_name)

        attemptsMade100 = Badge.objects.create(
            id_name='attempts-made-100',
            display_name='Made one hundred question attempts!',
            description='Attempted one hundred questions',
            icon_name='img/icons/badges/icons8-attempt-made-gold-50.png',
            badge_tier=4
        )
        print("Loaded badge: " + attemptsMade100.id_name)

        attemptsMade10 = Badge.objects.create(
            id_name='attempts-made-10',
            display_name='Made ten question attempts!',
            description='Attempted ten questions',
            icon_name='img/icons/badges/icons8-attempt-made-silver-50.png',
            badge_tier=3,
            parent=attemptsMade100
        )
        print("Loaded badge: " + attemptsMade10.id_name)

        attemptsMade5 = Badge.objects.create(
            id_name='attempts-made-5',
            display_name='Made five question attempts!',
            description='Attempted five questions',
            icon_name='img/icons/badges/icons8-attempt-made-bronze-50.png',
            badge_tier=2,
            parent=attemptsMade10
        )
        print("Loaded badge: " + attemptsMade5.id_name)

        attemptsMade1 = Badge.objects.create(
            id_name='attempts-made-1',
            display_name='Made your first question attempt!',
            description='Attempted one question',
            icon_name='img/icons/badges/icons8-attempt-made-black-50.png',
            badge_tier=1,
            parent=attemptsMade5
        )
        print("Loaded badge: " + attemptsMade1.id_name)

        consecutiveDays28 = Badge.objects.create(
            id_name='consecutive-days-28',
            display_name='Worked on coding every day for four weeks!',
            description='Attempted at least one question every day for four weeks',
            icon_name='img/icons/badges/icons8-calendar-28-50.png',
            badge_tier=5
        )
        print("Loaded badge: " + consecutiveDays28.id_name)

        consecutiveDays21 = Badge.objects.create(
            id_name='consecutive-days-21',
            display_name='Worked on coding every day for three weeks!',
            description='Attempted at least one question every day for three weeks',
            icon_name='img/icons/badges/icons8-calendar-21-50.png',
            badge_tier=4,
            parent=consecutiveDays28
        )
        print("Loaded badge: " + consecutiveDays21.id_name)

        consecutiveDays14 = Badge.objects.create(
            id_name='consecutive-days-14',
            display_name='Worked on coding every day for two weeks!',
            description='Attempted at least one question every day for two weeks',
            icon_name='img/icons/badges/icons8-calendar-14-50.png',
            badge_tier=3,
            parent=consecutiveDays21
        )
        print("Loaded badge: " + consecutiveDays14.id_name)

        consecutiveDays7 = Badge.objects.create(
            id_name='consecutive-days-7',
            display_name='Worked on coding every day for one week!',
            description='Attempted at least one question every day for one week',
            icon_name='img/icons/badges/icons8-calendar-7-50.png',
            badge_tier=2,
            parent=consecutiveDays14
        )
        print("Loaded badge: " + consecutiveDays7.id_name)

        consecutiveDays2 = Badge.objects.create(
            id_name='consecutive-days-2',
            display_name='Worked on coding for two days in a row!',
            description='Attempted at least one question two days in a row',
            icon_name='img/icons/badges/icons8-calendar-2-50.png',
            badge_tier=1,
            parent=consecutiveDays7
        )
        print("Loaded badge: " + consecutiveDays2.id_name)

        print("All badges loaded!\n")
