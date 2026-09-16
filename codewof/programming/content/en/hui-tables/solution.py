guests = int(input("How many guests? "))
tables = guests // 8
if guests % 8 != 0:
    tables += 1
print(tables)
