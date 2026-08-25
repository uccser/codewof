def long_words(words):
    result = []
    for word in words:
        if len(word) > 4:
            result.append(word)
    return result
