def count_warmer(temperatures, threshold):
    count = 0
    for temperature in temperatures:
        if temperature > threshold:
            count += 1
    return count
