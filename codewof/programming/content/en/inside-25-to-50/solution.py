def inside_or_outside(number, is_inside):
    if is_inside:
        if number < 25 or number > 50:
            return True
        else:
            return False
    else:
        if number >= 25 and number <= 50:
            return True
        else:
            return False
