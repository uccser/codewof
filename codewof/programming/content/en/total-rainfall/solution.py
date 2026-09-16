def total_rainfall(readings):
    total = 0
    for reading in readings:
        if reading > 0:
            total += reading
    return total
