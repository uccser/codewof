first = input("Name 1: ")
second = input("Name 2: ")
third = input("Name 3: ")
longest = first
if len(second) > len(longest):
    longest = second
if len(third) > len(longest):
    longest = third
print(longest)
