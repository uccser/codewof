def running_totals(numbers):
    result = []
    total = 0
    for number in numbers:
        total += number
        result.append(total)
    return result
