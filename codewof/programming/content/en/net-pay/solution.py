def net_pay(hours, rate):
    pay = hours * rate
    tax = pay * 20 / 100
    return pay - tax
