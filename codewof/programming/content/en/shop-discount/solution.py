price = float(input("Price: "))
if price >= 100:
    price = price - price * 10 / 100
print(price)
