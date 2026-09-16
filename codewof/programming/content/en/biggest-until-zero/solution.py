biggest = 0
number = int(input("Number: "))
while number != 0:
    if number > biggest:
        biggest = number
    number = int(input("Number: "))
print(biggest)
