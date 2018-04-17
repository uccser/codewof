from django.shortcuts import render
from django.views import generic

from .models import Question

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'questions/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.order_by('question_text')