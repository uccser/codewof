def check_danger_level(is_dark, is_wet):
    if is_dark is True and is_wet is True:
        print('The driving conditions are currently VERY dangerous!!')
    elif is_dark is True or is_wet is True:
        print('The driving conditions are currently dangerous!')
    else:
        print("It is a nice day for a drive.")


# todo: make this a debug question where the qoute in 'it's' string issue


check_danger_level(True, True)
check_danger_level(True, False)
check_danger_level(False, True)
check_danger_level(False, False)
