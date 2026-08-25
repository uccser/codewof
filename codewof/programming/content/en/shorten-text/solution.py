def shorten(text):
    if len(text) > 10:
        return text[:10] + "..."
    else:
        return text
