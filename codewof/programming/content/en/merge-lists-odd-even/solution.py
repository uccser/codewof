def merge_lists(list_1, list_2):
    result = []
    for num in list_1:
        if (num % 2 != 0):
            result.append(num)
    
    for num in list_2:
        if (num % 2 == 0):
            result.append(num)
    
    return result
