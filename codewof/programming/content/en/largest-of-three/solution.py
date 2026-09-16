first = int(input("Number 1: "))
second = int(input("Number 2: "))
third = int(input("Number 3: "))
largest = first
if second > largest:
    largest = second
if third > largest:
    largest = third
print(largest)
