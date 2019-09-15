def duck_goose(string):
    string = string.lower()
    num_goose = string.count('goose')
    num_duck = string.count('duck')

    return num_goose == num_duck
