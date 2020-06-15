from http import HTTPStatus
from django.test import TestCase, override_settings
from django.urls import reverse
from style.models import Error


class LanguageStatisticsViewTest(TestCase):

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
    def test_language_statistics_view_with_valid_slug(self):
        kwargs = {
            'language': 'python3',
        }
        url = reverse('style:language_statistics', kwargs=kwargs)
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
    def test_language_statistics_view_with_invalid_slug(self):
        kwargs = {
            'language': 'xyz',
        }
        url = reverse('style:language_statistics', kwargs=kwargs)
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
    def test_language_statistics_view_basic_context(self):
        kwargs = {
            'language': 'python3',
        }
        url = reverse('style:language_statistics', kwargs=kwargs)
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

    @override_settings(STYLE_CHECKER_LANGUAGES={
        'python3': {
            'name': 'Python 3',
            'slug': 'python3',
            'svg-icon': 'devicon-python.svg',
            'checker-config': '',
            'example_code': '',
        },
    })
    def test_language_statistics_view_valid_issues_context(self):
        error1 = Error(
            language='python3',
            code='error1',
            count=10,
        )
        error1.save()
        error2 = Error(
            language='python3',
            code='error2',
            count=20,
        )
        error2.save()
        error3 = Error(
            language='python3',
            code='error3',
            count=30,
        )
        error3.save()
        kwargs = {
            'language': 'python3',
        }
        url = reverse('style:language_statistics', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertQuerysetEqual(
            response.context['issues'],
            [
                '<Error: python3 - error3>',
                '<Error: python3 - error2>',
                '<Error: python3 - error1>',
            ]
        )
        self.assertEqual(
            response.context['max_count'],
            30
        )
