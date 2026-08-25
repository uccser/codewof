def chat_with_matt():
    print("Hi, my name is Matt and I love to chat!")
    print()
    print("What is your name?")
    name = input()
    if name.lower().startswith("m"):
        print("Your name starts with an M as well!")
    elif name.lower().endswith("t"):
        print("We both have names ending with t!")
    else:
        print("It is nice to meet you" + name + "!")
    print("Thanks for the chat!")
    print()
    print("Goodbye")
