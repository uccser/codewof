def count_vowels(text):
    count = 0
    for letter in text:
        if letter.lower() in "aeiou":
            count += 1
    return count
