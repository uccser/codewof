"""Helper functions for determining file paths for uploads."""

from os.path import join
from datetime import datetime
from pytz import timezone

# This is duplicated here to avoid circular dependency with settings file
TIME_ZONE = 'NZ'


def get_upload_path_for_date(category):
    """Create upload path for file by date.
    Args:
        category (str): Name for directory to upload to.

    Returns:
        String of path for upload.
    """
    return join(category, datetime.now(timezone(TIME_ZONE)).strftime('%Y/%m/%d'))
