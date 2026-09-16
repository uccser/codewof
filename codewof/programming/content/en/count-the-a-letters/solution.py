word = input("Word: ").lower()
count = 0
for letter in word:
    if letter == "a":
        count += 1
print(count)
