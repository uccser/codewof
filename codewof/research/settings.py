"""Settings for research application.

The research application is written to perform research on the
entire website at once, not allowing anyone to access the website
unless they pass a series of conditions checked by middleware.

If multiple groups needs to be checked, then the website is deployed
multiple times, each with their own configuration listed here.
"""

import datetime
from django.utils.timezone import make_aware

# Master switch for research features
RESEARCH_ACTIVE = False

# Dates (stored in NZ timezone as specified in settings)
START_DATETIME = make_aware(datetime.datetime(
    2021,  # Year
    10,  # Month
    1,  # Day
    hour=0,
    minute=0,
    second=0,
))
END_DATETIME = make_aware(datetime.datetime(
    2021,  # Year
    10,  # Month
    31,  # Day
    hour=11,
    minute=59,
    second=59,
))

# Accessiblity
USER_TYPES_ALLOWED = [
    'student',
    'teacher',
    'other',
]

# Appearance
SLUG = '2021-study'
TITLE = '2021 Study'
# Description is stored in research/study_description.html
