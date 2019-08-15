def smallest_number(numbers):
    smallest = numbers[0]
    for num in numbers:
        if num < smallest:
            smallest = num
            return smallest
