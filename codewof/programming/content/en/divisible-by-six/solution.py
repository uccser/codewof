def divisible_by_six(n):
    if n % 6 == 0:
        print(":)")
    elif n % 2 == 0 or n % 3 == 0:
        print(":|")
    else:
        print(":(")
