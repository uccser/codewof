"""Module for the custom Django load_questions command."""

from django.core.management.base import BaseCommand
from django.conf import settings
from utils.LoaderFactory import LoaderFactory


class Command(BaseCommand):
    """Required command class for the custom Django load_questions command."""

    help = 'Loads questions into the database'

    def handle(self, *args, **options):
        """Automatically called when the load_questions command is given."""
        factory = LoaderFactory()
        base_path = settings.QUESTIONS_BASE_PATH
        
        factory.difficulty_levels_loader(
            structure_filename='difficulty-levels.yaml',
            base_path=base_path
        ).load()

        factory.programming_concepts_loader(
            structure_filename='programming-concepts.yaml',
            base_path=base_path
        ).load()

        factory.question_contexts_loader(
            structure_filename='question-contexts.yaml',
            base_path=base_path
        ).load()

        factory.create_questions_loader(
            structure_filename='questions.yaml',
            base_path=base_path
        ).load()
