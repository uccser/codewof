def fizz_buzz(num):
    divisible_by_3 = num % 3 == 0
    divisible_by_5 = num % 5 == 0
    if divisible_by_3 and divisible_by_5:
        print('FizzBuzz')
    elif divisible_by_3:
        print('Fizz')
    elif divisible_by_5:
        print('Buzz')
    else:
        print(num)
