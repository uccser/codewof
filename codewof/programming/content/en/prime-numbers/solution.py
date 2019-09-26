number = int(input("Enter a positive integer: "))
if number < 2:
    print('No primes.')
else:
    print(2)
    for possible_prime in range(3, number + 1):
        prime = True
        for divisor in range(2, possible_prime):
            if (possible_prime % divisor) == 0:
                prime = False
                break
        if prime:
            print(possible_prime)
