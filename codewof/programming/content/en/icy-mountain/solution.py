def number_of_steps(up_amount, down_amount, height):
    if up_amount <= down_amount and height != 0:
        return False

    steps = 0
    current_height = 0

    while current_height < height:
        steps += 1
        current_height += up_amount

        if current_height < height:
            current_height -= down_amount

    return steps
