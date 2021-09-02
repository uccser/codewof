from research import settings


def get_study_for_context():
    context = {
        'slug': settings.SLUG,
        'title': settings.TITLE,
        'start': settings.START_DATETIME,
        'end': settings.END_DATETIME,
    }
    return context
