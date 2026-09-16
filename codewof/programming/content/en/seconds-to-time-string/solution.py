def time_string(total_seconds):
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return str(minutes) + "m " + str(seconds) + "s"
