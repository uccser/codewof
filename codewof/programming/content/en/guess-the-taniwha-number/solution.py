guess = int(input("Guess: "))
while guess != 7:
    if guess < 7:
        print("Too low!")
    else:
        print("Too high!")
    guess = int(input("Guess: "))
print("You found the taniwha!")
