def get_ticket_price(age):
    if age <= 5:
        price = 0
    elif age <= 12:
        price = 10
    else:
        price = 16
    return price
