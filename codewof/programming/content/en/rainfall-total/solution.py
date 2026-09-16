days = int(input("How many days? "))
total = 0
for _ in range(days):
    rainfall = int(input("Rainfall: "))
    total += rainfall
print(total)
