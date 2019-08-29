def carpark(hours):
    fee = 2.80
    total = 0
    if hours < 1:
        total = 0
    if hours > 1:
        hours = hours - 1
        total = hours * fee
    if total > 15:
        total = 15
    return total
