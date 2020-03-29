def factorial(x):
    if x < 1 or x > 10:
        return None
    else:
        answer = x
    while x > 1:
        x -= 1
        answer *= x
    return answer
