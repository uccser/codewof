import json
from ast import literal_eval

real_print = print
T = 0
n = 0

test_params = {{params}}
test_inputs = {{inputs}}

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
        user_output += '\n'
        printed[T] += user_output

temp = []
for params in test_params:
    params = [literal_eval(p) if p != '' else p for p in params]
    temp.append(params)

test_params = temp

{{solution}}

for i in range(N_test_cases):
    params = test_params[i]
    result = {{function_name}}(*params)
    returned[i] = result

results = {
    'expected_print': printed,
    'expected_return': returned,
}
real_print(json.dumps(results))
