from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from django.contrib.auth import login
from unittest import skip
import json

from questions.models import *
from questions.views import *


class ProfileViewTest(DjangoTestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        User.objects.create_user(username='john', email='john@uclive.ac.nz', password='onion')

    def login_user(self):
        login = self.client.login(username='john', password='onion')
        self.assertTrue(login)
    
    ### tests begin ###

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/profile/')
        self.assertRedirects(resp, '/login/?next=/profile/')

    def test_view_url_exists(self):
        self.login_user()
        resp = self.client.get('/profile/')
        self.assertEqual(resp.status_code, 200)
    
    def test_view_uses_correct_template(self):
        self.login_user()
        resp = self.client.get('/profile/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/profile.html')

class QuestionViewTest(DjangoTestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='john', email='john@uclive.ac.nz', password='onion')
        TestCase.objects.create(expected_output="hello world\n")
        question = Question.objects.create(title="Test question", question_text="Print hello world", question_type=1)
        question.test_cases.add(1)
        question.save()

        token_file = open("../../token_file.txt", "r")
        sphere_token = token_file.read().strip()
        Token.objects.create(name='sphere', token=sphere_token)

    def login_user(self):
        login = self.client.login(username='john', password='onion')
        self.assertTrue(login)

    ### tests begin ###

    def test_url_exists_not_logged_in(self):
        resp = self.client.get('/questions/1/')
        self.assertEqual(resp.status_code, 200)
    
    def test_url_exists_logged_in(self):
        self.login_user()
        resp = self.client.get('/questions/1/')
        self.assertEqual(resp.status_code, 200)

    def test_send_code(self):
        user_code = 'print("hello world")'
        payload = {'user_input': user_code, 'question': 1}
        resp = self.client.post('/ajax/send_code/', payload)
        result = json.loads(resp.content.decode('utf-8'))
        self.assertIn('id', list(result.keys()))
        submission_id = result['id']
        return submission_id


