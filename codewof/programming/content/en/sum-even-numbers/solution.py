def sum_evens(numbers):
    total = 0
    for number in numbers:
        if number % 2 == 0:
            total += number
    return total
