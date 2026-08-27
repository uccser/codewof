def count_odds(numbers):
    count = 0
    for number in numbers:
        if number % 2 != 0:
            count += 1
    return count
