import django_filters
from programming.models import (
    Question,
    DifficultyLevel,
    ProgrammingConcepts,
    QuestionContexts,
)
from django.db.models import Q


class QuestionFilter(django_filters.FilterSet):
    # contexts=django_filters.filters.CharFilter(method="contexts_filter")

    concepts = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=ProgrammingConcepts.objects.prefetch_related('parent')
    )
    contexts = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=QuestionContexts.objects.prefetch_related('parent')
    )

    class Meta:
        model = Question
        fields = {'difficulty_level', 'concepts', 'contexts'}

    # def contexts_filter(self, queryset, name, value):
    #     return Question.objects.filter(
    #         Q(contexts__name__icontains=value) | Q(contexts__parent__name__icontains=value)
    #     )
