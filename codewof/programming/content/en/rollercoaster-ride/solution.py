def ride_the_rollercoaster(age, with_an_adult):
    if age >= 12:
        print("You can ride the rollercoaster")
    elif age <= 5:
        print("Sorry, you cannot ride the rollercoaster")
    else:
        if with_an_adult is True:
            print("You can ride the rollercoaster")
        else:
            print("Sorry, you cannot ride the rollercoaster")
