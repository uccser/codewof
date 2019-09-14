year = int(input("Year? "))
if year % 400 == 0:
    print('Is a leap year')
elif (year % 4 == 0) and (year % 100 != 0):
    print('Is a leap year')
else:
    print('Is not a leap year')