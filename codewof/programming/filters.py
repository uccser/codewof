import django_filters
from programming.models import Question

class QuestionFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Question
        fields = {'title'}