"""Factory for creating loader objects."""

from codewof.management.commands._QuestionsLoader import QuestionsLoader


class LoaderFactory:
    """Factory for creating loader objects."""

    def create_questions_loader(self, **kwargs):
        """Create questions loader."""
        return QuestionsLoader(**kwargs)
