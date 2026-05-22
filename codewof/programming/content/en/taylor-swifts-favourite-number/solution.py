def taylor_swifts_favourite_number(number_guess):
    taylors_favourite_number = 13
    if number_guess == taylors_favourite_number:
        print("This is Taylor Swifts favourite number!")
    elif number_guess < taylors_favourite_number:
        print(f"This number is {taylors_favourite_number - number_guess} less than Taylor Swifts favourite number.")
    else:
        print(f"This number is {number_guess - taylors_favourite_number} more than Taylor Swifts favourite number.")

