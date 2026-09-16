def wind_warning(speed):
    if speed >= 100:
        print("Severe gale")
    elif speed >= 60:
        print("Strong wind")
    else:
        print("Calm enough")
