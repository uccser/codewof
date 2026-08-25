username = input("Username: ")
while " " in username:
    print("Usernames cannot contain spaces!")
    username = input("Username: ")
print("Welcome " + username + "!")
