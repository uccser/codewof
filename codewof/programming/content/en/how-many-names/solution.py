def number_of_names(word_list):
    total = 0
    for word in word_list:
        if word.istitle() is True:
            total += 1
    return total
