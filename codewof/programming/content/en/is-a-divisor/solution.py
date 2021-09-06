initial_number = int(input("Number: "))
number = int(input("Number: "))
while number != 0:
    if initial_number % number == 0:
        print(str(number) + " is a divisor")
    else:
        print(str(number) + " is not a divisor")
    number = int(input("Number: "))
