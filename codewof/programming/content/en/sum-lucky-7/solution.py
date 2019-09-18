def sum_lucky_7(numbers):
    total = 0
    for num in numbers:
        if num == 7:
            total += num * 2
        else:
            total += num
    print(total)
