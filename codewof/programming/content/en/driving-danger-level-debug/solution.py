def check_danger_level(is_dark, is_wet):
    if is_dark is True and is_wet is True:
        print('The driving conditions are currently VERY dangerous!!')
    elif is_dark is True or is_wet is True:
        print('The driving conditions are currently dangerous!')
    else:
        print("It's a nice day for a drive.")
