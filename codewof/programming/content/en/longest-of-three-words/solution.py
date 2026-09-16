first = input("Word 1: ")
second = input("Word 2: ")
third = input("Word 3: ")
longest = first
if len(second) > len(longest):
    longest = second
if len(third) > len(longest):
    longest = third
print(longest)
