def count_spaces(text):
    count = 0
    for char in text:
        if char == " ":
            count += 1
    return count
