def is_descending(items):
    result = True
    for i in range(1, len(items)):
        if items[i - 1] < items[i]:
            result = False
    return result
