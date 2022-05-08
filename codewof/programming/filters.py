"""Filters for programming application."""

import django_filters
from programming.models import (
    Question,
    DifficultyLevel,
    ProgrammingConcepts,
    QuestionContexts,
)
from programming.widgets import IndentCheckbox, DifficultyCheckbox, TypeCheckbox


class QuestionFilter(django_filters.FilterSet):
    """Filter for questions extends FilterSet.
    Allows for filtering of question type, difficulty level, concepts and contexts
    """

    difficulty_level = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=DifficultyLevel.objects.order_by('level'),
        widget=DifficultyCheckbox,
    )

    concepts = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=ProgrammingConcepts.objects.prefetch_related('parent').order_by('number'),
        widget=IndentCheckbox,
        conjoined=False,
    )

    contexts = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=QuestionContexts.objects.prefetch_related('parent').order_by('number'),
        widget=IndentCheckbox,
        conjoined=False,
    )

    question_type = django_filters.filters.AllValuesMultipleFilter(
        widget=TypeCheckbox,
    )

    class Meta:
        """Meta options for Filter. Sets which model and fields are filtered."""

        model = Question
        fields = {'difficulty_level', 'concepts', 'contexts', 'question_type'}
