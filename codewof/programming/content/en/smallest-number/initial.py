def smallest_number(list):
    smallest = 0
    for num in list[1:]:
        if num < smallest:
            smallest = num
    
    print(smallest)
