string = input("What words start with H? ")
while string.lower().startswith("h"):
    print("Yes, {} starts with H.".format(string))
    string = input("What words start with H? ")
print("No, {} doesn't start with H!".format(string))
