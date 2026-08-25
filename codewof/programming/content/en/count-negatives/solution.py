def count_negatives(numbers):
    total = 0
    for number in numbers:
        if number < 0:
            total += 1
    return total
