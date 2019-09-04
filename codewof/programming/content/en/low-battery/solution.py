def battery_is_low(percent):
    if percent < 20:
        is_low = True
    else:
        is_low = False
    return is_low
