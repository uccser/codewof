def reverse_list(items):
    result = []
    for item in items:
        result = [item] + result
    return result
