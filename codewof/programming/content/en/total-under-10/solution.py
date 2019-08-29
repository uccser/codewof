def total_under_ten(numbers):
    total = 0
    for number in numbers:
        if number < 10:
            total = total + number
    return total
