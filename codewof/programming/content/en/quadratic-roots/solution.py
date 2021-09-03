def number_of_roots(a, b, c):
    discriminant = b ** 2 - 4 * a * c

    if discriminant > 0:
        num_roots = 2
    elif discriminant < 0:
        num_roots = 0
    else:
        num_roots = 1

    return num_roots
