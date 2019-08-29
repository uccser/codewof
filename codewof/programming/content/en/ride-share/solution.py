def rideshare(km, airportfee):
    fee = 0
    tripfee = 0
    if airportfee == "yes":
        fee = fee + 6.5
    totalfee = km * 2.7
    total = totalfee + fee
    total = total * 1.15
    total = round(total, 2)
    print(total)