home = int(input("Home score: "))
away = int(input("Away score: "))
if home > away:
    print("Home win")
elif away > home:
    print("Away win")
else:
    print("Draw")
