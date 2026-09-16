def coldest(temperatures):
    lowest = temperatures[0]
    for temperature in temperatures:
        if temperature < lowest:
            lowest = temperature
    return lowest
