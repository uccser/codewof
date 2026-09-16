students = int(input("How many students? "))
buses = students // 45
if students % 45 != 0:
    buses += 1
print(buses)
