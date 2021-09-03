initial_number = int(input("Number: "))
number = int(input("Number: "))
while number != 0:
    is_divisor = initial_number % number == 0
    print(f"{number} is a divisor" if is_divisor else f"{number} is not a divisor")
    number = int(input("Number: "))
