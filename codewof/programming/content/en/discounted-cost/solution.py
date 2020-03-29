def discounted_cost(price, discount_percent):
    discount = price * discount_percent / 100
    cost = price - discount
    return cost
