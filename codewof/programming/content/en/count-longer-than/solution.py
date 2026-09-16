def count_longer_than(words, length):
    count = 0
    for word in words:
        if len(word) > length:
            count += 1
    return count
