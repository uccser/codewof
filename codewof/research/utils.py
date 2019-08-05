"""Utility functions for the research module."""

import importlib
from django.conf import settings


def get_consent_form(form_class_name):
    """Return form class for research consent form.

    Args:
        form_module: Name of form class (str).

    Returns:
        Instance of form class.
    """
    form_module = importlib.import_module(settings.RESEARCH_CONSENT_FORMS_PACKAGE)
    form_class = getattr(form_module, form_module_name)
    form = form_class()
    return form
