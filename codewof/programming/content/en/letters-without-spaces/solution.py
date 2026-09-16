sentence = input("Sentence: ")
count = 0
for char in sentence:
    if char != " ":
        count += 1
print(count)
