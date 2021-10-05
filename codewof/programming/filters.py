from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter
from programming.models import Question, DifficultyLevel, QuestionContexts, ProgrammingConcepts
from django.db import models

class QuestionFilter(FilterSet):
    # contexts=django_filters.filters.CharFilter(method="contexts_filter")
    difficulty_level = ModelChoiceFilter(queryset=DifficultyLevel.objects.all())
    contexts = ModelMultipleChoiceFilter(queryset=QuestionContexts.objects.all())
    concepts = ModelMultipleChoiceFilter(queryset=ProgrammingConcepts.objects.all())
    
    class Meta:
        model = Question
        fields = {'difficulty_level', 'concepts', 'contexts'}

    # def contexts_filter(self, queryset, name, value):
    #     return Question.objects.filter(
    #         Q(contexts__name__icontains=value) | Q(contexts__parent__name__icontains=value)
    #     )