def reverse_string(string):
    reverse = ''
    for char in range(len(string) - 1, -1, -1):
        reverse += string[char]
    
    print(reverse)
