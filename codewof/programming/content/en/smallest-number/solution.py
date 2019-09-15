def smallest_number(list):
    smallest = list[0]
    for num in list[1:]:
        if num < smallest:
            smallest = num

    print(smallest)
