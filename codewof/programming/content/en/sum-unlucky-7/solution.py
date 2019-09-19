def sum_unlucky_7(numbers):
    total = 0
    ignore_next = False
    for num in numbers:
        if num == 7:
            ignore_next = True
        else:
            if ignore_next:
                ignore_next = False
            else:
                total += num

    print(total)
