def digit_sum(number):
    total = 0
    for digit in str(number):
        total += int(digit)
    return total
