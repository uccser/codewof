import json

real_print = print
T = 0
n = 0

test_params = {{params}}
test_inputs = {{inputs}}
test_outputs = {{outputs}}
test_returns = {{returns}}


N_test_cases = {{n_test_cases}}
correct = [False] * N_test_cases
printed = [''] * N_test_cases
returned = [None] * N_test_cases

def update_globals():
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
        user_output += '\n'
        printed[T] += user_output

{% if is_func %}
{{user_code}}

for i in range(N_test_cases):
    params = test_params[i]
    result = {{function_name}}(*params)
    update_globals()

    returned[i] = result
    if result == test_returns[i]:
        correct[i] = True
    expected_output = test_outputs[i]
    if printed[i].rstrip() != expected_output.rstrip():
        correct[i] = False
{% else %}

def run_user_program():
    {{user_code}}

for i in range(N_test_cases):
    run_user_program()
    update_globals()

    correct[i] = True
    expected_output = test_outputs[i]
    if printed[i].rstrip() != expected_output.rstrip():
        correct[i] = False
{% endif %}

{% if is_buggy %}
correct = [not bool_value for bool_value in correct]
{% endif %}

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