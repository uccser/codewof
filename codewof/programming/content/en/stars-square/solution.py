def stars_square(size):
    if size <= 0:
        print("Too small!")
    else:
        for i in range(size):
            print("#" * size)
