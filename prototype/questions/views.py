from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F

import requests
import time
import datetime
import random
import json

from .forms import *
from .models import *

class LastAccessMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.last_login = datetime.datetime.now()
            request.user.save(update_fields=['last_login'])

            profile = request.user.profile
            today = datetime.date.today()

            login_days = profile.loginday_set.order_by('-day')
            if len(login_days) > 1:
                request.user.last_login = login_days[1].day
                request.user.save(update_fields=['last_login'])

            if not login_days.filter(day=today).exists():
                day = LoginDay(profile=profile)
                day.save()

        return super(LastAccessMixin, self).dispatch(request, *args, **kwargs)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password successfully updated')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form })


def get_random_question(request, current_question_id):
    valid_question_ids = []
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        completed_questions = Question.objects.filter(profile=user.profile, attempt__passed_tests=True)
        valid_question_ids = [question.id for question in Question.objects.all() if question not in completed_questions]
    else:
        valid_question_ids = [question.id for question in Question.objects.all()]
    
    if current_question_id in valid_question_ids:
        valid_question_ids.remove(current_question_id)

    question_number = random.choice(valid_question_ids)
    return redirect('/questions/' + str(question_number))


def save_attempt(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        profile = user.profile
        question = Question.objects.get(pk=request.POST.get('question'))
        
        user_code = request.POST.get('user_input')
        passed_tests = json.loads(request.POST.get('passed_tests'))
        is_save = json.loads(request.POST.get('is_save'))

        attempt = Attempt(profile=profile, question=question, user_code=user_code, passed_tests=passed_tests, is_save=is_save)
        attempt.save()

        if not is_save:
            max_points_from_attempts = 3
            points_for_correct = 5
            n_attempts = len(Attempt.objects.filter(question=question, profile=profile, is_save=False))

            previous_corrects = Attempt.objects.filter(question=question, profile=profile, passed_tests=True, is_save=False)
            is_first_correct = len(previous_corrects) == 1

            points_to_add = 0
            if n_attempts <= max_points_from_attempts:
                points_to_add += 1

            if passed_tests and is_first_correct:
                points_from_previous_attempts = n_attempts if n_attempts < max_points_from_attempts else max_points_from_attempts
                points_to_add += (points_for_correct - points_from_previous_attempts)
            
            profile.points = F('points') + points_to_add
            print(points_to_add)
            profile.save()


    result = {}
    return JsonResponse(result)


def save_goal_choice(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        profile = user.profile

        goal_choice = request.POST.get('goal_choice')
        profile.goal = int(goal_choice)
        profile.save()
    
    return JsonResponse({})


def get_consecutive_sections(days_logged_in):
    consecutive_sections = []

    today = days_logged_in[0]
    previous_section = [today]
    for day in days_logged_in[1:]:
        if day == previous_section[-1] - datetime.timedelta(days=1):
            previous_section.append(day)
        else:
            consecutive_sections.append(previous_section)
            previous_section = [day]
    
    consecutive_sections.append(previous_section)
    return consecutive_sections


def check_badge_conditions(user):
    earned_badges = user.profile.earned_badges.all()

    creation_badge = Badge.objects.get(id_name="create-account")
    if creation_badge not in earned_badges:
        new_achievement = Earned(profile=user.profile, badge=creation_badge)
        new_achievement.save()

    login_badges = Badge.objects.filter(id_name__contains="login")
    for login_badge in login_badges:
        if login_badge not in earned_badges:
            n_days = int(login_badge.id_name.split("-")[1])

            days_logged_in = LoginDay.objects.filter(profile=user.profile)
            days_logged_in = sorted(days_logged_in, key=lambda k: k.day, reverse=True)
            sections = get_consecutive_sections([d.day for d in days_logged_in])

            max_consecutive = len(max(sections, key=lambda k: len(k)))

            if max_consecutive >= n_days:
                new_achievement = Earned(profile=user.profile, badge=login_badge)
                new_achievement.save()

    solve_badges = Badge.objects.filter(id_name__contains="solve")
    for solve_badge in solve_badges:
        if solve_badge not in earned_badges:
            n_problems = int(solve_badge.id_name.split("-")[1])
            n_completed = len(Attempt.objects.filter(profile=user.profile, passed_tests=True, is_save=False))
            if n_completed >= n_problems:
                new_achievement = Earned(profile=user.profile, badge=solve_badge)
                new_achievement.save()



class ProfileView(LoginRequiredMixin, LastAccessMixin, generic.DetailView):
    """displays user's profile"""
    login_url = '/login/'
    redirect_field_name = 'next'
    template_name = 'registration/profile.html'
    model = User

    def get_object(self):
        if self.request.user.is_authenticated:
            return User.objects.get(username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = User.objects.get(username=self.request.user.username)
        questions = user.profile.attempted_questions.all()

        check_badge_conditions(user)

        context['goal'] = user.profile.goal
        context['all_badges'] = Badge.objects.all()
        context['past_5_weeks'] = [{'week': '17 Sep', 'n_attempts': 7}]

        t = datetime.date.today()
        today = datetime.datetime(t.year, t.month, t.day)
        last_monday = today - datetime.timedelta(days=today.weekday(), weeks=0)
        last_last_monday = today - datetime.timedelta(days=today.weekday(), weeks=1)

        past_5_weeks = []
        to_date = today
        for week in range(0, 5):
            from_date = today - datetime.timedelta(days=today.weekday(), weeks=week)
            attempts = Attempt.objects.filter(profile=user.profile, date__range=(from_date, to_date), is_save=False)

            label = str(week) + " weeks ago"
            if week == 0:
                label = "This week"
            elif week == 1:
                label = "Last week"

            past_5_weeks.append({'week': from_date, 'n_attempts': len(attempts), 'label': label})
            to_date = from_date
        context['past_5_weeks'] = past_5_weeks

        history = []
        for question in questions:
            if question.title not in [question['title'] for question in history]:
                attempts = Attempt.objects.filter(profile=user.profile, question=question, is_save=False)
                max_date = max(attempt.date for attempt in attempts)
                completed = any(attempt.passed_tests for attempt in attempts)
                history.append({'latest_attempt': max_date,'title': question.title,'n_attempts': len(attempts), 'completed': completed, 'id': question.pk})
        context['history'] = sorted(history, key=lambda k: k['latest_attempt'], reverse=True)
        return context


class IndexView(LastAccessMixin, generic.ListView):
    """displays list of skills"""
    template_name = 'questions/index.html'
    context_object_name = 'skill_list'

    def get_queryset(self):
        return SkillArea.objects.order_by('name')


class SkillView(LastAccessMixin, generic.DetailView):
    """displays list of questions which involve this skill"""
    template_name = 'questions/skill.html'
    context_object_name = 'skill'
    model = SkillArea


class QuestionView(LastAccessMixin, generic.DetailView):
    """displays question page"""
    template_name = 'questions/question.html'
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DebugInputForm()
        if self.request.user.is_authenticated:
            question = self.get_object()
            profile = self.request.user.profile
            all_attempts = Attempt.objects.filter(question=question, profile=profile)
            if len(all_attempts) > 0:
                context['previous_attempt'] = all_attempts.latest('date').user_code
        return context



BASE_URL = "http://36adab90.compilers.sphere-engine.com/api/v3/submissions/"
PYTHON = 116
COMPLETED = 0

COMMON_ABOVE = """
import json
from ast import literal_eval

real_print = print
T = 0
n = 0

"""

COMMON_MID = """
N_test_cases = len(test_returns)
correct = [False] * N_test_cases
printed = [''] * N_test_cases
returned = [None] * N_test_cases

def next_question():
    global T, n
    T += 1
    n = 0

def input(prompt=""):
    global n
    if n >= len(test_inputs[T]):
        raise EOFError()
    if len(prompt) > 1:
        print(prompt)
    test_input = test_inputs[T][n]
    n += 1
    return test_input

def print(user_output):
    if T < N_test_cases:
        user_output = str(user_output)
        user_output += '\\\\n'
        printed[T] += user_output

temp = []
for params in test_params:
    params = [literal_eval(p) if p != '' else p for p in params]
    temp.append(params)

test_params = temp

temp = []
for params in test_inputs:
    params = [literal_eval(p) if p != '' else p for p in params]
    temp.append(params)

test_inputs = temp

#test_outputs = [literal_eval(p) if p != '' else p for p in test_outputs]
test_returns = [literal_eval(p) if p != '' else p for p in test_returns]
"""

COMMON_BELOW = """
results = {
    'correct': correct,
    'printed': printed,
    'returned': returned,
    'inputs': test_inputs,
    'params': test_params,
    'expected_prints': test_outputs,
    'expected_returns': test_returns,
}
real_print(json.dumps(results))

"""

DEBUGGY_ABOVE = """
import json
from ast import literal_eval

real_print = print
T = 0
n = 0

"""

DEBUGGY_MID = """
N_test_cases = 1
printed = ['']
returned = [None]

def input(prompt=""):
    global n
    if n >= len(test_inputs[T]):
        raise EOFError()
    if len(prompt) > 1:
        print(prompt)
    test_input = test_inputs[T][n]
    n += 1
    return test_input

def print(user_output):
    if T < N_test_cases:
        user_output = str(user_output)
        user_output += '\\\\n'
        printed[T] += user_output

temp = []
for params in test_params:
    params = [literal_eval(p) if p != '' else p for p in params]
    temp.append(params)

test_params = temp
"""

DEBUGGY_BELOW = """
results = {
    'expected_print': printed,
    'expected_return': returned,
}
real_print(json.dumps(results))
"""


def format_test_data(test_cases):
    test_params = "\ntest_params = ["
    test_inputs = "\ntest_inputs = ["
    test_outputs = "\ntest_outputs = ["
    test_returns = "\ntest_returns = ["

    for case in test_cases:
        param_str = repr(case.function_params.split(',')) + ","
        input_str = repr(case.test_input.split('\n')) + ","
        output_str = repr(case.expected_output) + ","
        return_str = repr(case.expected_return) + ","

        test_params += param_str
        test_inputs += input_str
        test_outputs += output_str
        test_returns += return_str

    test_params = test_params[:-1] + "]\n"
    test_inputs = test_inputs[:-1] + "]\n"
    test_outputs = test_outputs[:-1] + "]\n"
    test_returns = test_returns[:-1] + "]\n"

    test_data = test_params + test_inputs + test_outputs + test_returns

    return test_data

def add_program_test_code(question, user_code):
    test_cases = question.test_cases.all()
    
    test_data = format_test_data(test_cases)

    repeated_user_code = ''
    for case in test_cases:
        repeated_user_code += user_code
        repeated_user_code += '\nnext_question()\n'

    processing = repeated_user_code + \
        '\nfor i in range(N_test_cases):\n' + \
        '    expected_output = test_outputs[i]\n' + \
        '    if printed[i] != expected_output:\n' + \
        '        correct[i] = False\n' + \
        '    else:\n' + \
        '        correct[i] = True\n'

    complete_code = COMMON_ABOVE + test_data + COMMON_MID + processing + COMMON_BELOW
    return complete_code


def add_function_test_code(question, user_code, expected_return, expected_output):
    
    if question.buggy_program:
        test_data = "\ntest_params = [" + repr(user_code.split(',')) + "]\n" + \
                    "\ntest_returns = [" + repr(expected_return) + "]\n" + \
                    "\ntest_inputs = [[]]\n" + \
                    "\ntest_outputs = [" + repr(expected_output) + "]\n"

        processing = question.buggy_program + \
            '\nfor i in range(N_test_cases):\n' + \
            '    params = test_params[i]\n' + \
            '    result = ' + question.function_name + '(*params)\n' + \
            '    returned[i] = result\n' + \
            '    if result != test_returns[i]:\n' + \
            '        correct[i] = True\n' + \
            '    expected_output = test_outputs[i]\n' + \
            '    if printed[i] != expected_output:\n' + \
            '        correct[i] = True\n'

        complete_code = COMMON_ABOVE + test_data + COMMON_MID + processing + COMMON_BELOW
        return complete_code

    else:
        test_cases = question.test_cases.all()
        test_data = format_test_data(test_cases)

        processing = user_code + \
            '\nfor i in range(N_test_cases):\n' + \
            '    params = test_params[i]\n' + \
            '    result = ' + question.function_name + '(*params)\n' + \
            '    returned[i] = result\n' + \
            '    if result == test_returns[i]:\n' + \
            '        correct[i] = True\n' + \
            '    next_question()\n' + \
            '    expected_output = test_outputs[i]\n' + \
            '    if printed[i] != expected_output:\n' + \
            '        correct[i] = False\n'

        complete_code = COMMON_ABOVE + test_data + COMMON_MID + processing + COMMON_BELOW
        return complete_code


def send_code(request):
    code = request.POST.get('user_input')
    expected_output = request.POST.get('expected_print')
    expected_return = request.POST.get('expected_return')
    question_id = request.POST.get('question')

    question = Question.objects.get(pk=question_id)

    if str(question.question_type) == 'Program':
        code = add_program_test_code(question, code, expected_output)
    elif str(question.question_type) == 'Function':
        code = add_function_test_code(question, code, expected_return, expected_output)
    
    token = "?access_token=" + Token.objects.get(pk='sphere').token

    response = requests.post(BASE_URL + token, data = {"language": PYTHON, "sourceCode": code})
    result = response.json()

    return JsonResponse(result)

def send_solution(request):
    test_input = request.POST.get('user_input')
    question_id = request.POST.get('question')

    question = Question.objects.get(pk=question_id)
    solution = question.solution

    test_data = "\ntest_params = [" + repr(test_input.split(',')) + "]\n"

    if str(question.question_type) == 'Function':
        solution = solution + \
            '\nfor i in range(N_test_cases):\n' + \
            '    params = test_params[i]\n' + \
            '    result = ' + question.function_name + '(*params)\n' + \
            '    returned[i] = result\n'

    code = DEBUGGY_ABOVE + test_data + DEBUGGY_MID + solution + DEBUGGY_BELOW
    token = "?access_token=" + Token.objects.get(pk='sphere').token

    response = requests.post(BASE_URL + token, data = {"language": PYTHON, "sourceCode": code})
    result = response.json()

    return JsonResponse(result)


def get_output(request):
    submission_id = request.POST.get('id')
    question_id = request.POST.get('question')

    token = "?access_token=" + Token.objects.get(pk='sphere').token

    params = {
        "withOutput": True, 
        "withStderr": True, 
        "withCmpinfo": True
    }
    response = requests.get(BASE_URL + submission_id + token, params=params)
    result = response.json()

    if result["status"] == COMPLETED:
        result["completed"] = True
    else:
        result["completed"] = False

    return JsonResponse(result)
    