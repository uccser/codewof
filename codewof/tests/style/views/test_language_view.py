from http import HTTPStatus
from django.test import TestCase, override_settings
from django.urls import reverse


class LanguageViewTest(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = 'en'

    @override_settings(STYLE_CHECKER_LANGUAGES={
        'python3': {
            'name': 'Python 3',
            'slug': 'python3',
            'svg-icon': 'devicon-python.svg',
            'checker-config': '',
            'example_code': '',
        },
    })
    def test_language_view_with_valid_slug(self):
        kwargs = {
            'language': 'python3',
        }
        url = reverse('style:language', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    @override_settings(STYLE_CHECKER_LANGUAGES={
        'python3': {
            'name': 'Python 3',
            'slug': 'python3',
            'svg-icon': 'devicon-python.svg',
            'checker-config': '',
            'example_code': '',
        },
    })
    def test_language_view_with_invalid_slug(self):
        kwargs = {
            'language': 'xyz',
        }
        url = reverse('style:language', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    @override_settings(STYLE_CHECKER_LANGUAGES={
        'python3': {
            'name': 'Python 3',
            'slug': 'python3',
            'svg-icon': 'devicon-python.svg',
            'checker-config': '',
            'example_code': '',
        },
    })
    def test_language_view_context(self):
        kwargs = {
            'language': 'python3',
        }
        url = reverse('style:language', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            response.context['language'],
            {
                'name': 'Python 3',
                'slug': 'python3',
                'svg-icon': 'devicon-python.svg',
                'checker-config': '',
                'example_code': '',
            }
        )
        self.assertEqual(
            response.context['language_header'],
            'style/language-components/python3-header.html'
        )
        self.assertEqual(
            response.context['language_subheader'],
            'style/language-components/python3-subheader.html'
        )
        self.assertEqual(
            response.context['language_js'],
            'js/style_checkers/python3.js'
        )
