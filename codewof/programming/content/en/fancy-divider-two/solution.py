def fancy_divider(divider_length):
    divider = ''
    for i in range(divider_length):
        if i % 2 == 0:
            divider += '='
        else:
            divider += '-'
    print(divider)
