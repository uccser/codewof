import django_filters
from programming.models import Question

class QuestionFilter(django_filters.FilterSet):
    
    class Meta:
        model = Question
        fields = {'difficulty_level', 'concepts', 'contexts'}