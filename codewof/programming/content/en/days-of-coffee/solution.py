def days_of_coffee(money, coffee_price):
    days = 0
    while money >= coffee_price:
        money -= coffee_price
        days += 1
    print('I can get coffee {} days in a row with ${:.2f} leftover.'.format(days, money))


days_of_coffee(8.00, 4.00)
days_of_coffee(12.49, 2.5)
days_of_coffee(12.50, 2.5)
days_of_coffee(12.51, 2.5)
days_of_coffee(0, 2.5)

