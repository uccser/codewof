"""Module for the custom Django load_achievements command."""

from django.core.management.base import BaseCommand
from programming.models import Achievement

# TODO: Consider relocating to a yaml file like the questions
ACHIEVEMENTS = [
    {
        'id_name': 'create-account',
        'display_name': 'Created an account!',
        'description': 'Created your very own account',
        'icon_name': 'img/icons/achievements/icons8-achievement-create-account-48.png',
        'achievement_tier': 0,
        'parent': None
    },
    {
        'id_name': 'questions-solved-100',
        'display_name': 'Solved one hundred questions!',
        'description': 'Solved one hundred questions',
        'icon_name': 'img/icons/achievements/icons8-question-solved-gold-50.png',
        'achievement_tier': 4,
        'parent': None
    },
    {
        'id_name': 'questions-solved-10',
        'display_name': 'Solved ten questions!',
        'description': 'Solved ten questions',
        'icon_name': 'img/icons/achievements/icons8-question-solved-silver-50.png',
        'achievement_tier': 3,
        'parent': 'questions-solved-100'
    },
    {
        'id_name': 'questions-solved-5',
        'display_name': 'Solved five questions!',
        'description': 'Solved five questions',
        'icon_name': 'img/icons/achievements/icons8-question-solved-bronze-50.png',
        'achievement_tier': 2,
        'parent': 'questions-solved-10'
    },
    {
        'id_name': 'questions-solved-1',
        'display_name': 'Solved one question!',
        'description': 'Solved your very first question',
        'icon_name': 'img/icons/achievements/icons8-question-solved-black-50.png',
        'achievement_tier': 1,
        'parent': 'questions-solved-5'
    },
    {
        'id_name': 'attempts-made-100',
        'display_name': 'Made one hundred question attempts!',
        'description': 'Attempted one hundred questions',
        'icon_name': 'img/icons/achievements/icons8-attempt-made-gold-50.png',
        'achievement_tier': 4,
        'parent': None
    },
    {
        'id_name': 'attempts-made-10',
        'display_name': 'Made ten question attempts!',
        'description': 'Attempted ten questions',
        'icon_name': 'img/icons/achievements/icons8-attempt-made-silver-50.png',
        'achievement_tier': 3,
        'parent': 'attempts-made-100'
    },
    {
        'id_name': 'attempts-made-5',
        'display_name': 'Made five question attempts!',
        'description': 'Attempted five questions',
        'icon_name': 'img/icons/achievements/icons8-attempt-made-bronze-50.png',
        'achievement_tier': 2,
        'parent': 'attempts-made-10'
    },
    {
        'id_name': 'attempts-made-1',
        'display_name': 'Made your first question attempt!',
        'description': 'Attempted one question',
        'icon_name': 'img/icons/achievements/icons8-attempt-made-black-50.png',
        'achievement_tier': 1,
        'parent': 'attempts-made-5'
    },
    {
        'id_name': 'consecutive-days-28',
        'display_name': 'Worked on coding every day for four weeks!',
        'description': 'Attempted at least one question every day for four weeks',
        'icon_name': 'img/icons/achievements/icons8-calendar-28-50.png',
        'achievement_tier': 5,
        'parent': None
    },
    {
        'id_name': 'consecutive-days-21',
        'display_name': 'Worked on coding every day for three weeks!',
        'description': 'Attempted at least one question every day for three weeks',
        'icon_name': 'img/icons/achievements/icons8-calendar-21-50.png',
        'achievement_tier': 4,
        'parent': 'consecutive-days-28'
    },
    {
        'id_name': 'consecutive-days-14',
        'display_name': 'Worked on coding every day for two weeks!',
        'description': 'Attempted at least one question every day for two weeks',
        'icon_name': 'img/icons/achievements/icons8-calendar-14-50.png',
        'achievement_tier': 3,
        'parent': 'consecutive-days-21'
    },
    {
        'id_name': 'consecutive-days-7',
        'display_name': 'Worked on coding every day for one week!',
        'description': 'Attempted at least one question every day for one week',
        'icon_name': 'img/icons/achievements/icons8-calendar-7-50.png',
        'achievement_tier': 2,
        'parent': 'consecutive-days-14'
    },
    {
        'id_name': 'consecutive-days-2',
        'display_name': 'Worked on coding for two days in a row!',
        'description': 'Attempted at least one question two days in a row',
        'icon_name': 'img/icons/achievements/icons8-calendar-2-50.png',
        'achievement_tier': 1,
        'parent': 'consecutive-days-7'
    },
    {
        'id_name': 'solved-difficulty-moderate-15',
        'display_name': 'Solved 15 moderate questions!',
        'description': 'Solved 15 questions from the moderate category',
        'icon_name': 'img/icons/achievements/icons8-question-solved-gold-50.png',
        'achievement_tier': 3,
        'parent': None
    },
    {
        'id_name': 'solved-difficulty-moderate-10',
        'display_name': 'Solved 10 moderate questions!',
        'description': 'Solved 10 questions from the moderate category',
        'icon_name': 'img/icons/achievements/icons8-question-solved-silver-50.png',
        'achievement_tier': 2,
        'parent': 'solved-difficulty-moderate-15'
    },
    {
        'id_name': 'solved-difficulty-moderate-5',
        'display_name': 'Solved 5 moderate questions!',
        'description': 'Solved 5 questions from the moderate category',
        'icon_name': 'img/icons/achievements/icons8-question-solved-bronze-50.png',
        'achievement_tier': 1,
        'parent': 'solved-difficulty-moderate-10'
    },
    {
        'id_name': 'solved-difficulty-easy-15',
        'display_name': 'Solved 15 easy questions!',
        'description': 'Solved 15 questions from the easy category',
        'icon_name': 'img/icons/achievements/icons8-question-solved-gold-50.png',
        'achievement_tier': 3,
        'parent': None
    },
    {
        'id_name': 'solved-difficulty-easy-10',
        'display_name': 'Solved 10 easy questions!',
        'description': 'Solved 10 questions from the easy category',
        'icon_name': 'img/icons/achievements/icons8-question-solved-silver-50.png',
        'achievement_tier': 2,
        'parent': 'solved-difficulty-easy-15'
    },
    {
        'id_name': 'solved-difficulty-easy-5',
        'display_name': 'Solved 5 easy questions!',
        'description': 'Solved 5 questions from the easy category',
        'icon_name': 'img/icons/achievements/icons8-question-solved-bronze-50.png',
        'achievement_tier': 1,
        'parent': 'solved-difficulty-easy-10'
    },
    {
        'id_name': 'solved-difficulty-difficult-15',
        'display_name': 'Solved 15 difficult questions!',
        'description': 'Solved 15 questions from the difficult category',
        'icon_name': 'img/icons/achievements/icons8-question-solved-gold-50.png',
        'achievement_tier': 3,
        'parent': None
    },
    {
        'id_name': 'solved-difficulty-difficult-10',
        'display_name': 'Solved 10 difficult questions!',
        'description': 'Solved 10 questions from the difficult category',
        'icon_name': 'img/icons/achievements/icons8-question-solved-silver-50.png',
        'achievement_tier': 2,
        'parent': 'solved-difficulty-difficult-15'
    },
    {
        'id_name': 'solved-difficulty-difficult-5',
        'display_name': 'Solved 5 difficult questions!',
        'description': 'Solved 5 questions from the difficult category',
        'icon_name': 'img/icons/achievements/icons8-question-solved-bronze-50.png',
        'achievement_tier': 1,
        'parent': 'solved-difficulty-difficult-10'
    },
    {
        'id_name': 'solved-difficulty-complex-15',
        'display_name': 'Solved 15 complex questions!',
        'description': 'Solved 15 questions from the complex category',
        'icon_name': 'img/icons/achievements/icons8-question-solved-gold-50.png',
        'achievement_tier': 3,
        'parent': None
    },
    {
        'id_name': 'solved-difficulty-complex-10',
        'display_name': 'Solved 10 complex questions!',
        'description': 'Solved 10 questions from the complex category',
        'icon_name': 'img/icons/achievements/icons8-question-solved-silver-50.png',
        'achievement_tier': 2,
        'parent': 'solved-difficulty-complex-15'
    },
    {
        'id_name': 'solved-difficulty-complex-5',
        'display_name': 'Solved 5 complex questions!',
        'description': 'Solved 5 questions from the complex category',
        'icon_name': 'img/icons/achievements/icons8-question-solved-bronze-50.png',
        'achievement_tier': 1,
        'parent': 'solved-difficulty-complex-10'
    },
    {
        'id_name': 'solved-concept-display-text-15',
        'display_name': 'Solved 15 display text questions!',
        'description': 'Solved 15 questions using the display text concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-gold-50.png',
        'achievement_tier': 3,
        'parent': None
    },
    {
        'id_name': 'solved-concept-display-text-10',
        'display_name': 'Solved 10 display text questions!',
        'description': 'Solved 10 questions using the display text concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-silver-50.png',
        'achievement_tier': 2,
        'parent': 'solved-concept-display-text-15'
    },
    {
        'id_name': 'solved-concept-display-text-5',
        'display_name': 'Solved 5 display text questions!',
        'description': 'Solved 5 questions using the display text concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-bronze-50.png',
        'achievement_tier': 1,
        'parent': 'solved-concept-display-text-10'
    },
    {
        'id_name': 'solved-concept-inputs-15',
        'display_name': 'Solved 15 input questions!',
        'description': 'Solved 15 questions using the input concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-gold-50.png',
        'achievement_tier': 3,
        'parent': None
    },
    {
        'id_name': 'solved-concept-inputs-10',
        'display_name': 'Solved 10 input questions!',
        'description': 'Solved 10 questions using the input concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-silver-50.png',
        'achievement_tier': 2,
        'parent': 'solved-concept-inputs-15'
    },
    {
        'id_name': 'solved-concept-inputs-5',
        'display_name': 'Solved 5 input questions!',
        'description': 'Solved 5 questions using the input concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-bronze-50.png',
        'achievement_tier': 1,
        'parent': 'solved-concept-inputs-10'
    },
    {
        'id_name': 'solved-concept-conditionals-15',
        'display_name': 'Solved 15 conditionals questions!',
        'description': 'Solved 15 questions using the conditionals concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-gold-50.png',
        'achievement_tier': 3,
        'parent': None
    },
    {
        'id_name': 'solved-concept-conditionals-10',
        'display_name': 'Solved 10 conditionals questions!',
        'description': 'Solved 10 questions using the conditionals concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-silver-50.png',
        'achievement_tier': 2,
        'parent': 'solved-concept-conditionals-15'
    },
    {
        'id_name': 'solved-concept-conditionals-5',
        'display_name': 'Solved 5 conditionals questions!',
        'description': 'Solved 5 questions using the conditionals concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-bronze-50.png',
        'achievement_tier': 1,
        'parent': 'solved-concept-conditionals-10'
    },
    {
        'id_name': 'solved-concept-loops-15',
        'display_name': 'Solved 15 loops questions!',
        'description': 'Solved 15 questions using the loops concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-gold-50.png',
        'achievement_tier': 3,
        'parent': None
    },
    {
        'id_name': 'solved-concept-loops-10',
        'display_name': 'Solved 10 loops questions!',
        'description': 'Solved 10 questions using the loops concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-silver-50.png',
        'achievement_tier': 2,
        'parent': 'solved-concept-loops-15'
    },
    {
        'id_name': 'solved-concept-loops-5',
        'display_name': 'Solved 5 loops questions!',
        'description': 'Solved 5 questions using the loops concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-bronze-50.png',
        'achievement_tier': 1,
        'parent': 'solved-concept-loops-10'
    },
    {
        'id_name': 'solved-concept-string-operations-15',
        'display_name': 'Solved 15 string operation questions!',
        'description': 'Solved 15 questions using the string operation concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-gold-50.png',
        'achievement_tier': 3,
        'parent': None
    },
    {
        'id_name': 'solved-concept-string-operations-10',
        'display_name': 'Solved 10 string operation questions!',
        'description': 'Solved 10 questions using the string operation concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-silver-50.png',
        'achievement_tier': 2,
        'parent': 'solved-concept-string-operations-15'
    },
    {
        'id_name': 'solved-concept-string-operations-5',
        'display_name': 'Solved 5 string operation questions!',
        'description': 'Solved 5 questions using the string operation concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-bronze-50.png',
        'achievement_tier': 1,
        'parent': 'solved-concept-string-operations-10'
    },
    {
        'id_name': 'solved-concept-lists-15',
        'display_name': 'Solved 15 lists questions!',
        'description': 'Solved 15 questions using the lists concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-gold-50.png',
        'achievement_tier': 3,
        'parent': None
    },
    {
        'id_name': 'solved-concept-lists-10',
        'display_name': 'Solved 10 lists questions!',
        'description': 'Solved 10 questions using the lists concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-silver-50.png',
        'achievement_tier': 2,
        'parent': 'solved-concept-lists-15'
    },
    {
        'id_name': 'solved-concept-lists-5',
        'display_name': 'Solved 5 lists questions!',
        'description': 'Solved 5 questions using the lists concept',
        'icon_name': 'img/icons/achievements/icons8-question-solved-bronze-50.png',
        'achievement_tier': 1,
        'parent': 'solved-concept-lists-10'
    },
    {
        'id_name': 'solved-context-real-world-applications-5',
        'display_name': 'Solved 5 real world application questions!',
        'description': 'Solved 5 questions in the real world application context',
        'icon_name': 'img/icons/achievements/icons8-question-solved-bronze-50.png',
        'achievement_tier': 1,
        'parent': None
    }
]


class Command(BaseCommand):
    """Required command class for the custom Django load_achievements command.

    Future plan: Create full loader like the load_questions command
    """

    help = 'Loads achievements into the database'

    def handle(self, *args, **options):
        """Automatically called when the load_achievements command is given."""
        all_achievements = {}

        for achievement in ACHIEVEMENTS:
            all_achievements[achievement['id_name']], created = Achievement.objects.update_or_create(
                id_name=achievement['id_name'],
                defaults={
                    'display_name': achievement['display_name'],
                    'description': achievement['description'],
                    'icon_name': achievement['icon_name'],
                    'achievement_tier': achievement['achievement_tier'],
                    'parent': None if achievement['parent'] is None else all_achievements[achievement['parent']]
                }
            )
            print("{} achievement: {}".format("Created" if created else "Updated", achievement['id_name']))

        print("{} achievements loaded!\n".format(len(all_achievements)))
