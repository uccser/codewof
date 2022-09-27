def speeding_tickets(car_speeds, speed_limit):
    total = 0
    for speed in car_speeds:
        if speed > speed_limit + 4:
            total = total + 1
    return total
