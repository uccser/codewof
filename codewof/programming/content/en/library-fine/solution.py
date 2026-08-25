def fine_in_cents(days_late):
    if days_late <= 3:
        return 0
    else:
        return (days_late - 3) * 25
