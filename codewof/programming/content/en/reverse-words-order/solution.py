def reverse_words(sentence):
    words = sentence.split()
    result = ''
    for word in words:
        result = word + ' ' + result
    return result[:-1]
