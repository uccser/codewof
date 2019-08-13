"""Module for the custom Django load_questions command."""

from django.core.management.base import BaseCommand
from django.conf import settings
from utils.LoaderFactory import LoaderFactory


class Command(BaseCommand):
    """Required command class for the custom Django load_questions command."""

    help = 'Loads questions into the database'

    def handle(self, *args, **options):
        """Automatically called when the load_questions command is given."""
        base_path = settings.QUESTIONS_BASE_PATH
        questions_structure_file = 'questions.yaml'
        factory = LoaderFactory()

        factory.create_questions_loader(
            structure_filename=questions_structure_file,
            base_path=base_path
        ).load()
