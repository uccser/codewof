def is_price_in_budget(price):
    if price >= 100 and price <= 500:
        is_in_budget = True
    else:
        is_in_budget = False
    return is_in_budget
