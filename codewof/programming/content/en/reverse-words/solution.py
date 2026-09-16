def reverse_words(sentence):
    reversed_words = []
    for word in sentence.split():
        reversed_words = [word] + reversed_words
    return " ".join(reversed_words)
