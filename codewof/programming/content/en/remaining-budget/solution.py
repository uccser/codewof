budget = int(input("Budget: "))
price = int(input("Price: "))
while price != 0:
    budget -= price
    price = int(input("Price: "))
print(budget)
