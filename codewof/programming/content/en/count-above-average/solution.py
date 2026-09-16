def count_above_average(numbers):
    average = sum(numbers) / len(numbers)
    count = 0
    for number in numbers:
        if number > average:
            count += 1
    return count
