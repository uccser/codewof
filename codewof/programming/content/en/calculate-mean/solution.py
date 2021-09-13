def mean(items):
    return sum(items) / len(items)


print(mean([2, 2, 2, 2]))
print(mean([0, 5, 0, 5]))
print(mean([1]))

one_to_twenty = list(range(1, 21))
print(one_to_twenty)
print(mean(one_to_twenty))
