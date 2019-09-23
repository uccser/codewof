def days_to_target(starting_population, target_population):
    population = starting_population
    days = 0
    while population < target_population:
        population = population * 2
        days = days + 1
    return days
