from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
import requests
import time

from .models import Question, SkillArea, TestCase, Token


class IndexView(generic.ListView):
    """displays list of skills"""
    template_name = 'questions/index.html'
    context_object_name = 'skill_list'

    def get_queryset(self):
        return SkillArea.objects.order_by('name')


class SkillView(generic.DetailView):
    """displays list of questions which involve this skill"""
    template_name = 'questions/skill.html'
    context_object_name = 'skill'
    model = SkillArea


class QuestionView(generic.DetailView):
    """displays question page"""
    template_name = 'questions/question.html'
    model = Question

BASE_URL = "http://36adab90.compilers.sphere-engine.com/api/v3/submissions/"
TOKEN = "?access_token=" + Token.objects.get(pk='sphere').token
PYTHON = 116
SUCCESS = 15

def send_code(request):
    code = request.POST.get('user_input')
    
    response = requests.post(BASE_URL + TOKEN, data = {"language": PYTHON, "sourceCode": code})
    result = {
       "data": response.json()
    }

    return JsonResponse(result)

def get_output(request):
    execution_id = request.GET.get('id')
    question_id = request.GET.get('question')

    data = {
        "status": -1
    }
    while data["status"] != 0:
        time.sleep(3)
        params = {
            "withOutput": True, 
            "withStderr": True, 
            "withCmpinfo": True
        }
        response = requests.get(BASE_URL + execution_id + TOKEN, params=params)
        data = response.json()

    if data["result"] == SUCCESS:
        output = data["output"]
        question = Question.objects.get(pk=question_id)
        test_cases = question.test_cases.all()
        expected_output = test_cases.first().expected_output

        if output[:-1] == expected_output:
            data["correct"] = True
        else:
            data["correct"] = False
    else:
        data["correct"] = False

    return JsonResponse(data)
    