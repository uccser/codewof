def tax_rate(income):
    if income <= 14000:
        return 10.5
    elif income <= 48000:
        return 17.5
    elif income <= 70000:
        return 30
    else:
        return 33
