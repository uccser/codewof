def count_long_words(words):
    count = 0
    for word in words:
        if len(word) > 5:
            count += 1
    return count
