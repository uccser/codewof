import datetime

from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from programming.models import Question, QuestionTypeProgram, Attempt, Like
from tests.codewof_test_data_generator import (
    generate_users,
    generate_questions,
    generate_attempts,
    generate_test_cases,
    generate_achievements,
    generate_likes
)
from programming.codewof_utils import check_achievement_conditions
from tests.conftest import user
import json

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
        generate_test_cases()

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

    def test_get_object_question_exists(self):
        self.login_user()
        question = QuestionTypeProgram.objects.get(slug='program-question-1')
        resp = self.client.get('/questions/{}/'.format(question.pk))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.context['question'],
            question
        )

    def test_get_object_question_does_not_exist(self):
        self.login_user()
        resp = self.client.get('/questions/{}/'.format('fake-primary-key'))
        self.assertEqual(resp.status_code, 404)

    def test_context_data(self):
        self.login_user()
        question = QuestionTypeProgram.objects.get(slug='program-question-1')
        resp = self.client.get('/questions/{}/'.format(question.pk))
        self.assertEqual(resp.status_code, 200)
        self.assertCountEqual(
            resp.context['test_cases'],
            question.test_cases.values(),
        )
        self.assertCountEqual(
            resp.context['test_cases_json'],
            json.dumps(list(question.test_cases.values())),
        )
        self.assertEqual(
            resp.context['question_js'],
            'js/question_types/{}.js'.format(question.QUESTION_TYPE),
        )
        self.assertEqual(
            resp.context['previous_attempt'],
            None,
        )


class CreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_questions()
        generate_attempts()

    def setUp(self):
        self.client = Client()

    def test_view_uses_correct_template(self):
        resp = self.client.get('/questions/create/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'programming/create.html')

    def test_context_object(self):
        user = User.objects.get(id=1)
        check_achievement_conditions(user.profile)  # make sure a program question has been answered

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
        generate_achievements()
        generate_attempts()
        generate_test_cases()

    def setUp(self):
        self.client = Client()

    def login_user(self):
        login = self.client.login(email='john@uclive.ac.nz', password='onion')
        self.assertTrue(login)

    def test_save_question_attempt_success_true(self):
        self.login_user()
        user = User.objects.get(id=1)
        check_achievement_conditions(user.profile)
        pk = Question.objects.get(slug='program-question-1').pk

        resp = self.client.post(
            '/ajax/save_question_attempt/',
            data={'question': pk, 'user_input': 'test', 'test_cases': {1: {'passed': True}}},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(200, resp.status_code)
        self.assertJSONEqual(
            str(resp.content, encoding='utf8'),
            {'success': True, 'curr_points': 50, 'point_diff': 0, 'achievements': ''}
        )

    def test_save_question_attempt_success_false(self):
        self.login_user()
        user = User.objects.get(id=1)
        check_achievement_conditions(user.profile)
        question = Question.objects.get(slug='program-question-1')

        attempt_one_resp = self.client.post(
            '/ajax/save_question_attempt/',
            data={'question': question.pk, 'user_input': 'test', 'test_cases': {1: {'passed': True}}},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(200, attempt_one_resp.status_code)
        self.assertJSONEqual(
            str(attempt_one_resp.content, encoding='utf8'),
            {'success': True, 'curr_points': 50, 'point_diff': 0, 'achievements': ''}
        )

        attempt_two_resp = self.client.post(
            '/ajax/save_question_attempt/',
            data={'question': question.pk, 'user_input': 'test', 'test_cases': {1: {'passed': True}}},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(200, attempt_two_resp.status_code)
        self.assertJSONEqual(
            str(attempt_two_resp.content, encoding='utf8'),
            {'success': False, 'message': 'Attempt not saved, same as previous attempt.'}
        )


class TestLikeAttempt(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_questions()
        generate_attempts()

    def setUp(self):
        self.john = User.objects.get(pk=1)
        self.sally = User.objects.get(pk=2)
        self.attempt = Attempt.objects.first()
        self.client = Client()

    def login_user(self, user):
        login = self.client.login(email=user.email, password='onion')
        self.assertTrue(login)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.post(reverse('programming:like_attempt', args=[self.attempt.pk]))
        self.assertRedirects(resp, '/accounts/login/?next=' + reverse('programming:like_attempt',
                                                                      args=[self.attempt.pk]))

    def test_like_attempt(self):
        self.login_user(self.sally)
        self.client.post(reverse('programming:like_attempt', args=[self.attempt.pk]))
        self.assertTrue(Like.objects.filter(user=self.sally, attempt=self.attempt).exists())

    def test_cannot_like_own_attempt(self):
        self.login_user(self.john)
        with self.assertRaisesMessage(Exception, "User cannot like their own attempt."):
            self.client.post(reverse('programming:like_attempt', args=[self.attempt.pk]))

    def test_cannot_like_attempt_twice(self):
        self.login_user(self.sally)
        Like(user=self.sally, attempt=self.attempt).save()
        with self.assertRaisesMessage(Exception, "Cannot like an attempt more than once."):
            self.client.post(reverse('programming:like_attempt', args=[self.attempt.pk]))
            self.assertEqual(len(Like.objects.filter(user=self.sally, attempt=self.attempt)), 1)


class TestUnLikeAttempt(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        generate_users(user)
        generate_questions()
        generate_attempts()
        generate_likes()

    def setUp(self):
        self.john = User.objects.get(pk=1)
        self.sally = User.objects.get(pk=2)
        self.attempt = Attempt.objects.first()
        self.unliked_attempt = Attempt.objects.filter(datetime=datetime.date(2019, 9, 9)).first()
        self.client = Client()

    def login_user(self, user):
        login = self.client.login(email=user.email, password='onion')
        self.assertTrue(login)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.delete(reverse('programming:unlike_attempt', args=[self.attempt.pk]))
        self.assertRedirects(resp, '/accounts/login/?next=' + reverse('programming:unlike_attempt',
                                                                      args=[self.attempt.pk]))

    def test_unlike_attempt(self):
        self.login_user(self.sally)
        self.client.delete(reverse('programming:unlike_attempt', args=[self.attempt.pk]))
        self.assertFalse(Like.objects.filter(user=self.sally, attempt=self.attempt).exists())

    def test_cannot_unlike_attempt_that_is_not_liked(self):
        self.login_user(self.sally)
        with self.assertRaisesMessage(Exception, "Can only unlike liked attempts."):
            self.client.delete(reverse('programming:unlike_attempt', args=[self.unliked_attempt.pk]))
