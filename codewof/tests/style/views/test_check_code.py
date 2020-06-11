from http import HTTPStatus
from django.test import TestCase, override_settings
from django.urls import reverse


class CheckCodeViewTest(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = 'en'

    def test_check_code_valid(self):
        pass

    def test_check_code_not_ajax(self):
        pass

    def test_check_code_code_empty(self):
        pass

    def test_check_code_code_too_long(self):
        pass

    def test_check_code_code_invalid_language(self):
        pass

    @override_settings(STYLE_CHECKER_LANGUAGES={})
    def test_check_code_with_no_languages(self):
        pass
