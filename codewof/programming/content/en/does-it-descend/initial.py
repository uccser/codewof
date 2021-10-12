def is_descending(items):
    result = True
    for i in range(1, len(items)):
        if i - 1 < i:
            result = False
    return result
