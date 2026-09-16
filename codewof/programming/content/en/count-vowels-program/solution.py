word = input("Word: ")
count = 0
for letter in word:
    if letter.lower() in "aeiou":
        count += 1
print(count)
