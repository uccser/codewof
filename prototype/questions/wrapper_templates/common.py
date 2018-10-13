import json

real_print = print
T = 0 # index of test case
I = 0 # index of input (for questions which ask for input more than once)

test_params = {{params}}
test_inputs = {{inputs}}
test_outputs = {{outputs}}
test_returns = {{returns}}


N_test_cases = {{n_test_cases}}
correct = [False] * N_test_cases
printed = [''] * N_test_cases
returned = [None] * N_test_cases

def update_globals():
    """reset I when moving onto next test case"""
    global T, I
    T += 1
    I = 0

def input(prompt=""):
    """overrides Python's built-in input function"""
    global I
    if I >= len(test_inputs[T]):
        raise EOFError()
    if len(prompt) > 1:
        print(prompt)
    test_input = test_inputs[T][I]
    I += 1
    return test_input

def print(user_output):
    """overrides Python's built-in print function"""
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
    if printed[i].rstrip() != test_outputs[i].rstrip():
        correct[i] = False
{% else %}

def run_user_program():
    {{user_code}}

for i in range(N_test_cases):
    run_user_program()
    update_globals()

    correct[i] = True
    if printed[i].rstrip() != test_outputs[i].rstrip():
        correct[i] = False
{% endif %}

{% if is_buggy %}
correct = [not bool_value for bool_value in correct]
{% endif %}

results = {
    'correct': correct,
    'printed': printed,
    'returned': [repr(r) for r in returned],
    'inputs': test_inputs,
    'params': [repr(t) for t in test_params],
    'expected_prints': test_outputs,
    'expected_returns': [repr(r) for r in test_returns],
}
real_print(json.dumps(results))