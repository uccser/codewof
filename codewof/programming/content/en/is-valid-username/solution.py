def is_valid_username(name):
    if len(name) >= 3 and len(name) <= 12:
        return True
    else:
        return False
