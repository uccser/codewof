def number_of_steps(up_amount, height):
    steps = 0
    current_height = 0

    while current_height < height:
        steps += 1
        current_height += up_amount

    return steps
