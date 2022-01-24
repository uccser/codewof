def days_of_coffee(money, coffee_price):
    days = 0
    while money >= 0:
        money -= coffee_price
        days += 1
    print('I can get coffee {} days in a row with ${:.2f} leftover.'.format(days, money))
