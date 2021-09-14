def remove_seal(container):
    if container[-1] == 'seal':
        container.pop()


test_tube = ['sediment', 'gold', 'murky water', 'seal']
remove_seal(test_tube)
print(test_tube)

test_tube = []
remove_seal(test_tube)
print(test_tube)

test_tube = ['sediment', 'gold', 'murky water', 'seal']
result = remove_seal(test_tube)
print(result == None)
