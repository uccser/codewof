from django.shortcuts import render
from django.views import generic

from .models import Question, SkillArea, TestCase


class IndexView(generic.ListView):
    """displays list of skills"""
    template_name = 'questions/index.html'
    context_object_name = 'skill_list'

    def get_queryset(self):
        return SkillArea.objects.order_by('name')


class SkillView(generic.ListView):
    """displays list of questions which involve this skill"""
    template_name = 'questions/skill.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.order_by('title')

class QuestionView(generic.DetailView):
    """displays list of questions which involve this skill"""
    template_name = 'questions/question.html'
    model = Question
    