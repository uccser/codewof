"""Filters for programming application."""

import django_filters
from programming.models import (
    Question,
    DifficultyLevel,
    ProgrammingConcepts,
    QuestionContexts,
)
from django import forms
from programming.widgets import IndentCheckbox


class QuestionFilter(django_filters.FilterSet):
    """Filter for questions extends FilterSet
    Allows for filtering of question type, difficulty level, concepts and contexts"""

    difficulty_level = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=DifficultyLevel.objects.order_by('level'),
        widget=forms.CheckboxSelectMultiple
    )

    concepts = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=ProgrammingConcepts.objects.prefetch_related('parent').order_by('number'),
        widget=IndentCheckbox,
        conjoined=True
    )

    contexts = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=QuestionContexts.objects.prefetch_related('parent').order_by('number'),
        widget=IndentCheckbox,
        conjoined=True
    )

    question_type = django_filters.filters.AllValuesMultipleFilter(
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        """Meta options for Filter. Sets which model and fields are filtered."""
        model = Question
        fields = {'difficulty_level', 'concepts', 'contexts', 'question_type'}
