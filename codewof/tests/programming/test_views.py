from django.test import Client, TestCase

from programming.models import Question

from codewof.tests.codewof_test_data_generator import (
    generate_users,
    generate_questions,
)

from codewof.tests.conftest import user


class QuestionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_questions()

    def setUp(self):
        self.client = Client()

    def login_user(self):
        login = self.client.login(email='john@uclive.ac.nz', password='onion')
        self.assertTrue(login)

    # tests begin
    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/questions/')
        self.assertRedirects(resp, '/accounts/login/?next=/questions/')

    def test_view_url_exists(self):
        self.login_user()
        resp = self.client.get('/questions/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login_user()
        resp = self.client.get('/questions/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'programming/question_list.html')

    def test_get_queryset(self):
        self.assertQuerysetEqual(
            Question.objects.all(),
            [
                '<Question: Test>',
                '<Question: Test>',
                '<Question: Test>',
                '<Question: Test>',
                '<Question: Test>',
            ],
            ordered=False
        )


class QuestionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_questions()

    def setUp(self):
        self.client = Client()

    def login_user(self):
        login = self.client.login(email='john@uclive.ac.nz', password='onion')
        self.assertTrue(login)

    # tests begin
    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/questions/1/')
        self.assertRedirects(resp, '/accounts/login/?next=/questions/1/')

    def test_view_url_exists(self):
        self.login_user()
        pk = Question.objects.get(slug='program-question-1').pk
        resp = self.client.get('/questions/{}/'.format(pk))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login_user()
        pk = Question.objects.get(slug='program-question-1').pk
        resp = self.client.get('/questions/{}/'.format(pk))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'programming/question.html')
