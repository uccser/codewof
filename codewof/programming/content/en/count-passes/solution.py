def count_passes(marks):
    total = 0
    for mark in marks:
        if mark >= 50:
            total += 1
    return total
