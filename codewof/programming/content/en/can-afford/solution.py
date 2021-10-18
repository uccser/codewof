def can_afford(balance):
    tablet = "Nothing"

    if balance >= 1000:
        tablet = "ePad"
    elif balance >= 500:
        tablet = "Noshiba Sandibook"

    return tablet
