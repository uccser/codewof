def fibonacci(limit):
    first = 0
    second = 1
    while second < limit:
        print(second)
        new = first + second
        first = second
        second = new
