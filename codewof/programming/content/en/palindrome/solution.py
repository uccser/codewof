def is_palindrome(word):
    result = True
    halfway_index = len(word) // 2

    for i in range(halfway_index):
        j = -(i + 1)
        if word[i] != word[j]:
            result = False
            break

    return result
