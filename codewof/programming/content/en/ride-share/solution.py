def calculate_ride_share(km, airport_fee):
    fee = 0
    if airport_fee:
        fee = fee + 6.5
    totalfee = km * 2.7
    total = totalfee + fee
    total = total * 1.15
    total = round(total, 2)
    print(total)
