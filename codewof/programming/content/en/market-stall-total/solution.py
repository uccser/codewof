count = int(input("How many items? "))
total = 0
for _ in range(count):
    price = int(input("Price: "))
    total += price
print(total)
