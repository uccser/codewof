"""Module for the testing custom Django load_style_errors commands."""

from django.test import TestCase
from django.core import management


class LoadStyleErrorsCommandTest(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"

    def test_load_style_errors_valid(self):
        management.call_command("load_style_errors")
