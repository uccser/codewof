def storage_is_full(occupied, capacity):
    percent = occupied / capacity * 100
    if percent >= 85:
        is_full = True
    else:
        is_full = False
    return is_full


print(storage_is_full(1, 10))
print(storage_is_full(9, 10))
print(storage_is_full(84, 100))
print(storage_is_full(85, 100))
print(storage_is_full(11, 10))
print(type(storage_is_full(1, 10)))




