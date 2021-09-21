import django_filters
from programming.models import Question

class QuestionFilter(django_filters.FilterSet):
    difficulty_level = django_filters.CharFilter(field_name="difficulty_level__name", lookup_expr='iexact')

    class Meta:
        model = Question
        fields = {'difficulty_level'}