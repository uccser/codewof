count = int(input("How many numbers? "))
total = 0
for _ in range(count):
    number = int(input("Number: "))
    total += number
print(total / count)
