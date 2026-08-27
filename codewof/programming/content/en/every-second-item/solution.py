def every_second(items):
    result = []
    for i in range(0, len(items), 2):
        result.append(items[i])
    return result
