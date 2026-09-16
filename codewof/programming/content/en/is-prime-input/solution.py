number = int(input("Number: "))
prime = number > 1
for divisor in range(2, number):
    if number % divisor == 0:
        prime = False
if prime:
    print("Prime")
else:
    print("Not prime")
