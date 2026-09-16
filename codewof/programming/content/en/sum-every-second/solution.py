def sum_every_second(numbers):
    total = 0
    for i in range(0, len(numbers), 2):
        total += numbers[i]
    return total
