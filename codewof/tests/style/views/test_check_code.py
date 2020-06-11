import json
from http import HTTPStatus
from django.test import TestCase, override_settings
from django.urls import reverse

SAMPLE_PROGRAM_1 = "print('Hello world!')"


class CheckCodeViewTest(TestCase):

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
    def test_check_code_valid(self):
        data = {
            'language': 'python3',
            'user_code': SAMPLE_PROGRAM_1,
        }
        url = reverse('style:check_code')
        response = self.client.post(
            url,
            json.dumps(data),
            'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        json_string = response.content
        response_data = json.loads(json_string)
        self.assertTrue(response_data['success'])

    def test_check_code_not_ajax(self):
        url = reverse('style:check_code')
        response = self.client.get(url)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        json_string = response.content
        response_data = json.loads(json_string)
        self.assertFalse(response_data['success'])

    def test_check_code_code_empty(self):
        data = {
            'language': 'python3',
            'user_code': '',
        }
        url = reverse('style:check_code')
        response = self.client.post(
            url,
            json.dumps(data),
            'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        json_string = response.content
        response_data = json.loads(json_string)
        self.assertFalse(response_data['success'])

    def test_check_code_code_too_long(self):
        data = {
            'language': 'python3',
            'user_code': '#' * 100000,
        }
        url = reverse('style:check_code')
        response = self.client.post(
            url,
            json.dumps(data),
            'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        json_string = response.content
        response_data = json.loads(json_string)
        self.assertFalse(response_data['success'])

    def test_check_code_code_invalid_language(self):
        data = {
            'language': 'not-a-language',
            'user_code': SAMPLE_PROGRAM_1,
        }
        url = reverse('style:check_code')
        response = self.client.post(
            url,
            json.dumps(data),
            'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        json_string = response.content
        response_data = json.loads(json_string)
        self.assertFalse(response_data['success'])

    @override_settings(STYLE_CHECKER_LANGUAGES={})
    def test_check_code_with_no_languages(self):
        data = {
            'language': 'python3',
            'user_code': SAMPLE_PROGRAM_1,
        }
        url = reverse('style:check_code')
        response = self.client.post(
            url,
            json.dumps(data),
            'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        json_string = response.content
        response_data = json.loads(json_string)
        self.assertFalse(response_data['success'])
