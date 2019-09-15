def sum_lucky_7(list):
    total = 0
    double_next = False
    for num in list:
        if num == 7:
            double_next = True
            total += num * 2
        else:
            if double_next:
                to_add = num * 2
                double_next = False
            else:
                to_add = num
            total += to_add

    print(total)
