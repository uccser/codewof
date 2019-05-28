# -*- coding: utf-8 -*-
"""Django settings for connecting via Google Cloud SQL Proxy."""

from .production import *  # noqa: F403

# DATABASE CONFIGURATION
# ----------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": 'django.contrib.gis.db.backends.postgis',
        "HOST": "cloud_sql_proxy",
        "PORT": "5432",
        "NAME": "codewof",
        "USER": env("GOOGLE_CLOUD_SQL_DATABASE_USERNAME"),  # noqa: F405
        "PASSWORD": env("GOOGLE_CLOUD_SQL_DATABASE_PASSWORD"),  # noqa: F405
        "ATOMIC_REQUESTS": True,
    }
}
