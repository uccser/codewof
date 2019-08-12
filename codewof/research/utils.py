"""Utility functions for the research module."""

import importlib
from research import settings


def get_consent_form_class(form_class_name):
    """Return form class for research consent form.

    Args:
        form_class_name: Name of form class (str).

    Returns:
        Instance of form class.
    """
    form_module = importlib.import_module(settings.RESEARCH_FORMS_MODULE)
    form_class = getattr(form_module, form_class_name)
    return form_class
