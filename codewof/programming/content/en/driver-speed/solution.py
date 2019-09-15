def check_speed(speed):
    if speed <= 50:
        print('Ok.')
    else:
        speed_over = speed - 50
        points = int(speed_over / 5)
        if points < 5:
            print(points)
        else:
            print("License suspended.")
