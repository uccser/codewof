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
COMPLETED = 0
PROGRAM = 1
FUNCTION = 2

PROGRAM_ABOVE = """
import json
n = 0
m = 0
correct = [False] * len(test_outputs)
def input(prompt=""):
    global n
    real_print(prompt)
    test_input = test_inputs[n]
    if n >= len(test_inputs):
        raise EOFError()
    n += 1
    return test_input
real_print = print
def print(user_output):
    global m
    if m < len(test_outputs):
        expected_output = test_outputs[m]
        if user_output == expected_output:
            correct[m] = True
        m += 1
"""

PROGRAM_BELOW = """
if n < len(test_inputs):
    raise Exception('Input was not called enough times')
real_print(json.dumps(correct))
"""

def add_program_test_code(question, user_code):
    test_cases = question.test_cases.all()
    
    test_inputs = "\ntest_inputs = ["
    test_outputs = "\ntest_outputs = ["
    repeated_user_code = """\n"""

    for case in test_cases:
        input_str = repr(case.test_input) + ", "
        output_str = repr(case.expected_output) + ", "
        code_str = user_code + "\n"

        test_inputs += input_str
        test_outputs += output_str
        repeated_user_code += code_str
        
    test_inputs = test_inputs[:-2] + "]\n"
    test_outputs = test_outputs[:-2] + "]\n"

    complete_code = test_inputs + test_outputs + PROGRAM_ABOVE + repeated_user_code + PROGRAM_BELOW

    return complete_code


def add_function_test_code(question, user_code):
    test_cases = question.test_cases.all()


def send_code(request):
    code = request.POST.get('user_input')
    question_id = request.POST.get('question')
    question = Question.objects.get(pk=question_id)

    if question.question_type == PROGRAM:
        code = add_program_test_code(question, code)
    elif question.question_type == FUNCTION:
        code = add_function_test_code(question, code)
    
    response = requests.post(BASE_URL + TOKEN, data = {"language": PYTHON, "sourceCode": code})
    result = response.json()

    return JsonResponse(result)

def get_output(request):
    submission_id = request.GET.get('id')
    question_id = request.GET.get('question')

    params = {
        "withOutput": True, 
        "withStderr": True, 
        "withCmpinfo": True
    }
    response = requests.get(BASE_URL + submission_id + TOKEN, params=params)
    result = response.json()

    if result["status"] == COMPLETED:
        result["completed"] = True
    else:
        result["completed"] = False

    return JsonResponse(result)
    