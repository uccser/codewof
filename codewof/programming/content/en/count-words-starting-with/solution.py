def count_starting_with(words, letter):
    count = 0
    for word in words:
        if word.lower().startswith(letter.lower()):
            count += 1
    return count
