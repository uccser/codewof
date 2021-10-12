def storage_is_full(occupied, capacity):
    percent = occupied / capacity * 100
    if percent >= 85:
        is_full = True
    else:
        is_full = False
    return is_full
