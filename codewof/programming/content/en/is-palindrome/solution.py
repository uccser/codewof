def is_palindrome(text):
    reverse = ''
    for char in text:
        reverse = char + reverse
    return text == reverse
