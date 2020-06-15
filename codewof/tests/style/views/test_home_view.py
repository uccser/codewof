from http import HTTPStatus
from django.test import TestCase, override_settings
from django.urls import reverse


class HomeViewTest(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = 'en'

    @override_settings(STYLE_CHECKER_LANGUAGES={})
    def test_home_with_no_languages(self):
        url = reverse('style:home')
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            response.context['languages'],
            dict()
        )

    @override_settings(STYLE_CHECKER_LANGUAGES={
        'python3': {
            'name': 'Python 3',
            'slug': 'python3',
            'svg-icon': 'devicon-python.svg',
            'checker-config': '',
            'example_code': '',
        },
    })
    def test_index_with_one_language(self):
        url = reverse('style:home')
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            response.context['languages'],
            {
                'python3': {
                    'name': 'Python 3',
                    'slug': 'python3',
                    'svg-icon': 'devicon-python.svg',
                    'checker-config': '',
                    'example_code': '',
                },
            }
        )

    @override_settings(STYLE_CHECKER_LANGUAGES={
        'python3': {
            'name': 'Python 3',
            'slug': 'python3',
            'svg-icon': 'devicon-python.svg',
            'checker-config': '',
            'example_code': '',
        },
        'ruby': {
            'name': 'Ruby',
            'slug': 'ruby',
            'svg-icon': 'devicon-ruby.svg',
            'checker-config': '',
            'example_code': '',
        },
    })
    def test_index_with_multiple_languages(self):
        url = reverse('style:home')
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            response.context['languages'],
            {
                'python3': {
                    'name': 'Python 3',
                    'slug': 'python3',
                    'svg-icon': 'devicon-python.svg',
                    'checker-config': '',
                    'example_code': '',
                },
                'ruby': {
                    'name': 'Ruby',
                    'slug': 'ruby',
                    'svg-icon': 'devicon-ruby.svg',
                    'checker-config': '',
                    'example_code': '',
                },
            }
        )
