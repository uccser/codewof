def check_steps(steps):
    if steps >= 10000:
        print("Goal reached!")
    else:
        print("You need " + str(10000 - steps) + " more steps.")
