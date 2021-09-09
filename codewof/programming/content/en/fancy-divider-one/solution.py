def fancy_divider(divider_length):
    if divider_length == 1:
        divider = '+'
    else:
        divider = '+' + '-' * (divider_length - 2) + '+'

    print(divider)
