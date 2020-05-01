from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from programming.models import Question

from codewof.tests.codewof_test_data_generator import (
    generate_users,
    generate_questions,
    generate_attempts,
)
from codewof.programming.codewof_utils import check_badge_conditions
from codewof.tests.conftest import user
User = get_user_model()


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


class CreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_questions()
        generate_attempts()

    def test_view_uses_correct_template(self):
        resp = self.client.get('/questions/create/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'programming/create.html')

    def test_context_object(self):
        user = User.objects.get(id=1)
        check_badge_conditions(user.profile) # make sure a program question has been answered

        resp = self.client.get('/questions/create/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.context['question_types'],
            [
                {'name': 'Program', 'count': 1, 'unanswered_count': 0},
                {'name': 'Function', 'count': 1, 'unanswered_count': 1},
                {'name': 'Parsons', 'count': 1, 'unanswered_count': 1},
                {'name': 'Debugging', 'count': 1, 'unanswered_count': 1},

            ]
        )


class SaveQuestionAttemptTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_questions()
        generate_attempts()

    def setUp(self):
        self.client = Client()

    def login_user(self):
        login = self.client.login(email='john@uclive.ac.nz', password='onion')
        self.assertTrue(login)

    def test_save_question_attempt(self):
        self.login_user()
        pk = Question.objects.get(slug='program-question-1').pk
        resp = self.client.post(
            'http://localhost:83/ajax/save_question_attempt/',
            data={'question': pk, 'user_input': 'test', 'test_cases': {1: {'passed': True}}},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(200, resp.status_code)
