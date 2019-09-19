def sum_unlucky_7(list):
    total = 0
    ignore_next = False
    for num in list:
        if num == 7:
            ignore_next = True
        else:
            if ignore_next:
                ignore_next = false
                total += num

    print(total)
