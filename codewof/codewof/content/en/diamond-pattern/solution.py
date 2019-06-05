def diamond(x):
    if (x <= 1) or (x % 2 == 0):
        print("That isn't a diamond! Please enter a positive, odd integer.")
    else:
        spaces = (x - 1) // 2
        for i in range(1, x+1, 2):
            print((spaces * ' ') + (i * '*'))
            spaces -= 1

        spaces = 1
        for i in range(x - 2, 0, -2):
            print((spaces * ' ') + (i * '*'))
            spaces += 1
