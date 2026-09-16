today = int(input("Today: "))
yesterday = int(input("Yesterday: "))
if today > yesterday:
    print("Warmer today")
elif today < yesterday:
    print("Colder today")
else:
    print("Same as yesterday")
