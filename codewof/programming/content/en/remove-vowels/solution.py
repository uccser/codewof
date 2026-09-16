def remove_vowels(text):
    result = ""
    for letter in text:
        if letter.lower() not in "aeiou":
            result += letter
    return result
