def can_afford(balance):
    tablet = "Nothing"

    if balance >= 500:
        tablet = "Noshiba Sandibook"
    elif balance >= 1000:
        tablet = "ePad"

    return tablet
