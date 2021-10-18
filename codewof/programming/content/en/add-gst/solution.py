def add_gst(price, tax_percent):
    tax = price * tax_percent / 100
    cost = price + tax
    return cost
