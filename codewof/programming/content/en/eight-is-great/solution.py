def eight_is_great(a, b):
    if a == 8 or b == 8:
        return True
    elif abs(a - b) == 8:
        return True
    elif a + b == 8:
        return True
    else:
        return False
