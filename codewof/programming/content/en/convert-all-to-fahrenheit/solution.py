def all_to_fahrenheit(temperatures):
    result = []
    for temperature in temperatures:
        result.append(temperature * 9 / 5 + 32)
    return result
