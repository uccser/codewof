from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
import requests

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


def send_code(request):
    code = request.POST.get('user_input')
    
    base_url = "http://36adab90.compilers.sphere-engine.com/api/v3/submissions/"
    token = "?access_token=" + Token.objects.get(pk='sphere').token
    
    response = requests.post(base_url + token, data = {"language": 116, "sourceCode": code})
    result = response.json()
    data = {
        "result": result
    }
    return JsonResponse(data)

def getOutput():
    print("sending")
    
    #get result from sphere engine
    #compare with expected output
    #show output and correct/incorrect flag
    