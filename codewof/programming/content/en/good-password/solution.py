password = input("What is the password? ")
while len(password) < 5:
    print("No, this password is not good enough")
    password = input("What is the password? ")
print("Thank you, your password is good enough")
