def first_letters(sentence):
    result = ""
    words = sentence.split()
    for word in words:
        result += word[0]
    return result
