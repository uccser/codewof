word = input("Word: ")
count = 0
for letter in word.lower():
    if letter in "aeiou":
        count += 1
print(count)
