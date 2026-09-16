def count_negatives(numbers):
    count = 0
    for number in numbers:
        if number < 0:
            count += 1
    return count
