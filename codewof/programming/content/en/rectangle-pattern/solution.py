def rectangle(width, height):
    if width <= 0 or height <= 0:
        print("That isn't a rectangle!")
    else:
        for i in range(height):
            print(width * "#")
