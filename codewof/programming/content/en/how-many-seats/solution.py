def total_seats(vehicles):
    total = 0
    for vehicle in vehicles:
        if vehicle == "car":
            total += 5
        if vehicle == "truck":
            total += 3
        if vehicle == "bus":
            total += 20
    return total
