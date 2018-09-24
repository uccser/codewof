from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import requests
import time
import datetime
import random
import json
from ast import literal_eval
import jinja2

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
                day.full_clean()
                day.save()

        return super(LastAccessMixin, self).dispatch(request, *args, **kwargs)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.full_clean()
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
            form.full_clean()
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

    if len(valid_question_ids) < 1:
        url = '/'
    else:
        question_number = random.choice(valid_question_ids)
        url = '/questions/' + str(question_number)
    return redirect(url)


def add_points(question, profile, passed_tests):
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
    
    profile.points += points_to_add
    profile.full_clean()
    profile.save()


def save_attempt(request):
    request_json = json.loads(request.body.decode('utf-8'))
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        profile = user.profile
        question = Question.objects.get(pk=request_json['question'])
        
        user_code = request_json['user_input']
        passed_tests = request_json['passed_tests']
        is_save = request_json['is_save']

        attempt = Attempt(profile=profile, question=question, user_code=user_code, passed_tests=passed_tests, is_save=is_save)
        attempt.full_clean()
        attempt.save()

        if not is_save:
            add_points(question, profile, passed_tests)

    result = {}
    return JsonResponse(result)


def save_goal_choice(request):
    request_json = json.loads(request.body.decode('utf-8'))
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        profile = user.profile

        goal_choice = request_json['goal_choice']
        profile.goal = int(goal_choice)
        profile.full_clean()
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

    try:
        creation_badge = Badge.objects.get(id_name="create-account")
        if creation_badge not in earned_badges:
            new_achievement = Earned(profile=user.profile, badge=creation_badge)
            new_achievement.full_clean()
            new_achievement.save()
    except (Badge.DoesNotExist):
        pass

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
                new_achievement.full_clean()
                new_achievement.save()

    solve_badges = Badge.objects.filter(id_name__contains="solve")
    for solve_badge in solve_badges:
        if solve_badge not in earned_badges:
            n_problems = int(solve_badge.id_name.split("-")[1])
            n_completed = Attempt.objects.filter(profile=user.profile, passed_tests=True, is_save=False)
            n_distinct = n_completed.values("question__pk").distinct().count()
            if n_distinct >= n_problems:
                new_achievement = Earned(profile=user.profile, badge=solve_badge)
                new_achievement.full_clean()
                new_achievement.save()


def get_past_5_weeks(user):
    t = datetime.date.today()
    today = datetime.datetime(t.year, t.month, t.day)
    last_monday = today - datetime.timedelta(days=today.weekday(), weeks=0)
    last_last_monday = today - datetime.timedelta(days=today.weekday(), weeks=1)

    past_5_weeks = []
    to_date = today
    for week in range(0, 5):
        from_date = today - datetime.timedelta(days=today.weekday(), weeks=week)
        attempts = Attempt.objects.filter(profile=user.profile, date__range=(from_date, to_date + datetime.timedelta(days=1)), is_save=False)
        distinct_questions_attempted = attempts.values("question__pk").distinct().count()

        label = str(week) + " weeks ago"
        if week == 0:
            label = "This week"
        elif week == 1:
            label = "Last week"

        past_5_weeks.append({'week': from_date, 'n_attempts': distinct_questions_attempted, 'label': label})
        to_date = from_date
    return past_5_weeks


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
        context['past_5_weeks'] = get_past_5_weeks(user)

        history = []
        for question in questions:
            if question.title not in [question['title'] for question in history]:
                attempts = Attempt.objects.filter(profile=user.profile, question=question, is_save=False)
                if len(attempts) > 0:
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

        question = Question.objects.get_subclass(pk=self.get_object().pk)
        if isinstance(question, ProgrammingFunction):
            subclass = "programming_func"
        elif isinstance(question, Programming):
            subclass = "programming"
        elif isinstance(question, BuggyFunction):
            subclass = "buggy_func"
        elif isinstance(question, Buggy):
            subclass = "buggy"
        else:
            subclass = "parsons"

        context['question_subclass'] = subclass

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


def format_test_data(test_cases, is_function_type):
    test_params = "\ntest_params = ["
    test_inputs = "\ntest_inputs = ["
    test_outputs = "\ntest_outputs = ["
    test_returns = "\ntest_returns = ["

    for case in test_cases:
        if is_function_type:
            param_str = repr(case.function_params.split(',')) + ","
            return_str = repr(case.expected_return) + ","
            test_params += param_str
            test_returns += return_str

        input_str = repr(case.test_input.split('\n')) + ","
        output_str = repr(case.expected_output) + ","
        test_inputs += input_str
        test_outputs += output_str

    if is_function_type:
        test_params = test_params[:-1] + "]\n"
        test_returns = test_returns[:-1] + "]\n"
    else:
        test_params += "]\n"
        test_returns += "]\n"

    test_inputs = test_inputs[:-1] + "]\n"
    test_outputs = test_outputs[:-1] + "]\n"

    test_data = test_params + test_inputs + test_outputs + test_returns
    return test_data

def add_program_test_code(question, user_code):
    test_cases = question.programming.testcaseprogram_set.all()
    test_data = format_test_data(test_cases, is_function_type=False)

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

def add_buggy_program_test_code(code):
    # TODO
    return code

def add_function_test_code(question, user_code):
    test_cases = question.programming.programmingfunction.testcasefunction_set.all()
    test_data = format_test_data(test_cases, is_function_type=True)

    processing = user_code + \
        '\nfor i in range(N_test_cases):\n' + \
        '    params = test_params[i]\n' + \
        '    result = ' + question.programming.programmingfunction.function_name + '(*params)\n' + \
        '    returned[i] = result\n' + \
        '    if result == test_returns[i]:\n' + \
        '        correct[i] = True\n' + \
        '    next_question()\n' + \
        '    expected_output = test_outputs[i]\n' + \
        '    if printed[i] != expected_output:\n' + \
        '        correct[i] = False\n'

    complete_code = COMMON_ABOVE + test_data + COMMON_MID + processing + COMMON_BELOW
    return complete_code

def add_buggy_function_test_code(question, user_params, expected_output, expected_return):
    test_data = "\ntest_params = [" + repr(user_params.split(',')) + "]\n" + \
                "\ntest_returns = [" + repr(expected_return) + "]\n" + \
                "\ntest_inputs = [[]]\n" + \
                "\ntest_outputs = [" + repr(expected_output) + "]\n"

    processing = question.buggy.buggy_program + \
        '\nfor i in range(N_test_cases):\n' + \
        '    params = test_params[i]\n' + \
        '    result = ' + question.buggy.buggyfunction.function_name + '(*params)\n' + \
        '    returned[i] = result\n' + \
        '    if result != test_returns[i]:\n' + \
        '        correct[i] = True\n' + \
        '    expected_output = test_outputs[i]\n' + \
        '    if printed[i] != expected_output:\n' + \
        '        correct[i] = True\n'

    complete_code = COMMON_ABOVE + test_data + COMMON_MID + processing + COMMON_BELOW
    return complete_code


def send_code(request):
    request_json = json.loads(request.body.decode('utf-8'))
    user_input = request_json['user_input']
    question_id = request_json['question']
    question = Question.objects.get_subclass(pk=question_id)

    # ###
    # if isinstance(question, ProgrammingFunction):
    #     code = add_function_test_code(question, user_input)
    # elif isinstance(question, Programming):
    #     code = add_program_test_code(question, user_input)
    # elif isinstance(question, BuggyFunction):
    #     code = add_buggy_function_test_code(question, user_input, expected_output, expected_return)
    # elif isinstance(question, Buggy):
    #     code = add_buggy_program_test_code(user_input)

    # ###

    template_loader = jinja2.FileSystemLoader(searchpath="questions/wrapper_templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "common.py"
    template = template_env.get_template(template_file)

    is_func = isinstance(question, ProgrammingFunction) or isinstance(question, BuggyFunction)
    is_buggy = isinstance(question, Buggy)

    if is_func:
        if is_buggy:
            func_name = question.buggy.buggyfunction.function_name
        else:
            func_name = question.programming.programmingfunction.function_name

    if is_buggy:
        user_stdin = request_json['buggy_stdin']
        inputs = [user_stdin.split('\n')]
        expected_output = request_json['expected_print']
        outputs = [expected_output]
        if is_func:
            user_input = "[" + user_input + "]"
            try:
                test_params = literal_eval(user_input)
            except:
                message = "Input formatted incorrectly. Must be valid comma-separated python."
                result = {
                    'error': message
                }
                return JsonResponse(result)
            params = [test_params]
            print(request.body.decode('utf-8'))
            expected_return = request_json['expected_return']
            returns = [expected_return]
        
        user_input = question.buggy.buggy_program
    else:
        if is_func:
            test_cases = question.programming.programmingfunction.testcasefunction_set.all()
        else:
            test_cases = question.programming.testcaseprogram_set.all()

        params = [case.function_params.split(',') for case in test_cases]
        inputs = [case.test_input.split('\n') for case in test_cases]
        outputs = [case.expected_output for case in test_cases]
        returns = [case.expected_return for case in test_cases]

    context_variables = {
        'params': repr(params),
        'inputs': repr(inputs), 
        'outputs': repr(outputs),
        'returns': repr(returns),
        'is_func': is_func,
        'is_buggy': is_buggy,
        'user_code': user_input.replace('/t', '    '),
        'function_name': func_name
    }
    code = template.render(**context_variables)
    print(code)
    token = "?access_token=" + Token.objects.get(pk='sphere').token

    response = requests.post(BASE_URL + token, data = {"language": PYTHON, "sourceCode": code})
    result = response.json()

    return JsonResponse(result)

def send_solution(request):
    request_json = json.loads(request.body.decode('utf-8'))
    test_input = request_json['user_input']
    question_id = request_json['question']

    question = Question.objects.get_subclass(pk=question_id)
    solution = question.solution
    
    template_loader = jinja2.FileSystemLoader(searchpath="questions/wrapper_templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "template.py"
    template = template_env.get_template(template_file)

    context_variables = {
        'params': repr(test_input.split(',')),
        'solution': solution,
        'function_name': question.buggy.buggyfunction.function_name
    }
    code = template.render(**context_variables)

    token = "?access_token=" + Token.objects.get(pk='sphere').token

    response = requests.post(BASE_URL + token, data = {"language": PYTHON, "sourceCode": code})
    result = response.json()

    return JsonResponse(result)


def get_output(request):
    request_json = json.loads(request.body.decode('utf-8'))
    submission_id = request_json['id']
    question_id = request_json['question']

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
    