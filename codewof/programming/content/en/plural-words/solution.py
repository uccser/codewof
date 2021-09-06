string = input("What words are plural and end with s? ")
while string.lower().endswith("s"):
    print("Yes, {} ends with s.".format(string))
    string = input("What words are plural and end with s? ")
print("No, {} doesn't end with s!".format(string))
