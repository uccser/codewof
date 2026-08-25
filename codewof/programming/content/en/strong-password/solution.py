password = input("Password: ")
while len(password) < 8:
    print("Too short!")
    password = input("Password: ")
print("Password accepted!")
