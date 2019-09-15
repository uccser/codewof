def inside_25_to_50(number, outside_mode):
    if outside_mode:
        if number >= 25 and number <= 50:
            print('True')
        else:
            print('False')

    else:
        if number < 25 or number > 50:
            print('True')
        else:
            print('False')
