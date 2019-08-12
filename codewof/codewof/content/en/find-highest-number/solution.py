def find_highest_number(numbers):
    highest_number = numbers[0]
    for num in numbers:
        if num > highest_number:
            highest_number = num
    return highest_number
