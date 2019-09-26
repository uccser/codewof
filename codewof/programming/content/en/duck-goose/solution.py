string = input("?")
num_goose = string.count('goose')
num_duck = string.count('duck')
if num_goose == num_duck:
    print("Equal amount")
else:
    print("Different amount")
