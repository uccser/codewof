def inside_or_outside(number, is_inside):
    if is_inside is True:
        if number >= 25 and number <= 50:
            print('True')
        else:
            print('False')

    else:
        if number < 25 or number > 50:
            print('True')
        else:
            print('False')
