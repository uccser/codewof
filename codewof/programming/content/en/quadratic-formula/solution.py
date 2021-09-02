from math import sqrt


def get_roots(a, b, c):
    roots = None
    discriminant = b ** 2 - 4 * a * c
    if discriminant >= 0:
        root1 = round((-b + sqrt(discriminant)) / (2 * a), 2)

        if discriminant > 0:
            root2 = round((-b - sqrt(discriminant)) / (2 * a), 2)
            roots = (root1, root2) if root1 > root2 else (root2, root1)
        else:
            roots = root1

    return roots
