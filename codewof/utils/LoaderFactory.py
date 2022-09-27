"""Factory for creating loader objects."""

from programming.management.commands._QuestionsLoader import QuestionsLoader
from programming.management.commands._DifficultiesLoader import DifficultiesLoader
from programming.management.commands._ProgrammingConceptsLoader import ProgrammingConceptsLoader
from programming.management.commands._QuestionContextsLoader import QuestionContextsLoader


class LoaderFactory:
    """Factory for creating loader objects."""

    def difficulty_levels_loader(self, **kwargs):
        """Difficulty levels loader."""
        return DifficultiesLoader(**kwargs)

    def programming_concepts_loader(self, **kwargs):
        """Programming concepts loader."""
        return ProgrammingConceptsLoader(**kwargs)

    def question_contexts_loader(self, **kwargs):
        """Question contexts loader."""
        return QuestionContextsLoader(**kwargs)

    def create_questions_loader(self, **kwargs):
        """Create questions loader."""
        return QuestionsLoader(**kwargs)
