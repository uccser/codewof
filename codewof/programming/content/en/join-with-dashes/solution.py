def join_with_dashes(words):
    result = ''
    for word in words:
        result += word + '-'
    return result[:-1]
