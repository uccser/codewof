def remove_short_words(words):
    result = []
    for word in words:
        if len(word) > 3:
            result.append(word)
    return result
