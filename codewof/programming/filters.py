import django_filters
from programming.models import (
    Question,
    DifficultyLevel,
    ProgrammingConcepts,
    QuestionContexts,
)
from django.db.models import Q
from django import forms
from programming.widgets import IndentCheckbox


class QuestionFilter(django_filters.FilterSet):
    difficulty_level=django_filters.filters.ModelMultipleChoiceFilter(
        queryset=DifficultyLevel.objects.all().order_by('level'),
        widget=forms.CheckboxSelectMultiple,
        conjoined=True
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

    class Meta:
        model = Question
        fields = {'difficulty_level', 'concepts', 'contexts'}

    # def contexts_filter(self, queryset, name, value):
    #     return Question.objects.filter(
    #         Q(contexts__name__icontains=value) | Q(contexts__parent__name__icontains=value)
    #     )
