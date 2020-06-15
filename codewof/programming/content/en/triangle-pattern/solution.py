def triangle(x):
    if x <= 1:
        print("That isn't a triangle!")
    else:
        for i in range(1, x + 1):
            print(i * '*')
