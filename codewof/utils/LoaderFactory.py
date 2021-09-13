"""Factory for creating loader objects."""

from programming.management.commands._QuestionsLoader import QuestionsLoader
from programming.management.commands._DifficultiesLoader import DifficultiesLoader


class LoaderFactory:
    """Factory for creating loader objects."""

    def difficulty_levels_loader(self, **kwargs):
        """Difficulty levels loader"""
        return DifficultiesLoader(**kwargs)

    def create_questions_loader(self, **kwargs):
        """Create questions loader."""
        return QuestionsLoader(**kwargs)
