# from django.test import TestCase as DjangoTestCase
# from django.contrib.auth.models import User
# from django.contrib.auth import login
# from unittest import skip
# import json
# import time
# import datetime

# from questions.models import *
# from questions.views import *


# class ProfileViewTest(DjangoTestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # never modify this object in tests
#         User.objects.create_user(username='john', email='john@uclive.ac.nz', password='onion')

#     def login_user(self):
#         login = self.client.login(username='john', password='onion')
#         self.assertTrue(login)

#     ### tests begin ###

#     def test_redirect_if_not_logged_in(self):
#         resp = self.client.get('/profile/')
#         self.assertRedirects(resp, '/login/?next=/profile/')

#     def test_view_url_exists(self):
#         self.login_user()
#         resp = self.client.get('/profile/')
#         self.assertEqual(resp.status_code, 200)

#     def test_view_uses_correct_template(self):
#         self.login_user()
#         resp = self.client.get('/profile/')
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, 'registration/profile.html')


# class BadgeViewTest(DjangoTestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # never modify this object in tests
#         user = User.objects.create_user(username='john', email='john@uclive.ac.nz', password='onion')
#         LoginDay.objects.create(profile=user.profile)
#         Badge.objects.create(id_name="create-account", display_name="test", description="test")
#         Badge.objects.create(id_name="login-3", display_name="test", description="test")
#         Badge.objects.create(id_name="solve-1", display_name="test", description="test")

#     def test_new_user_awards_create_account(self):
#         user = User.objects.get(pk=1)
#         check_badge_conditions(user)
#         badge = Badge.objects.get(id_name="create-account")
#         earned = Earned.objects.filter(profile=user.profile, badge=badge)
#         self.assertEquals(len(earned), 1)

#     def test_doesnt_award_twice_create_account(self):
#         user = User.objects.get(pk=1)
#         badge = Badge.objects.get(id_name="create-account")
#         Earned.objects.create(profile=user.profile, badge=badge)
#         check_badge_conditions(user)

#         earned = Earned.objects.filter(profile=user.profile, badge=badge)
#         self.assertEquals(len(earned), 1)

#     def test_adding_unknown_badge_doesnt_break(self):
#         Badge.objects.create(id_name="notrealbadge", display_name="test", description="test")
#         user = User.objects.get(pk=1)
#         check_badge_conditions(user)

#     def test_no_award_consecutive_login_2(self):
#         user = User.objects.get(pk=1)
#         login_day = LoginDay.objects.create(profile=user.profile)
#         yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
#         LoginDay.objects.select_for_update().filter(pk=2).update(day=yesterday.date())

#         check_badge_conditions(user)
#         badge = Badge.objects.get(id_name="login-3")
#         earned = Earned.objects.filter(profile=user.profile, badge=badge)
#         self.assertEquals(len(earned), 0)

#     def test_award_consecutive_login_3(self):
#         user = User.objects.get(pk=1)
#         LoginDay.objects.create(profile=user.profile)
#         yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
#         LoginDay.objects.select_for_update().filter(pk=2).update(day=yesterday.date())

#         LoginDay.objects.create(profile=user.profile)
#         day_before_yesterday = datetime.datetime.now() - datetime.timedelta(days=2)
#         LoginDay.objects.select_for_update().filter(pk=3).update(day=day_before_yesterday.date())

#         check_badge_conditions(user)
#         badge = Badge.objects.get(id_name="login-3")
#         earned = Earned.objects.filter(profile=user.profile, badge=badge)
#         self.assertEquals(len(earned), 1)

#     def test_award_consecutive_login_3_from_last_week(self):
#         user = User.objects.get(pk=1)
#         LoginDay.objects.create(profile=user.profile)
#         last_week3 = datetime.datetime.now() - datetime.timedelta(days=1, weeks=1)
#         LoginDay.objects.select_for_update().filter(pk=2).update(day=last_week3.date())

#         LoginDay.objects.create(profile=user.profile)
#         last_week2 = datetime.datetime.now() - datetime.timedelta(days=2, weeks=1)
#         LoginDay.objects.select_for_update().filter(pk=3).update(day=last_week2.date())

#         LoginDay.objects.create(profile=user.profile)
#         last_week1 = datetime.datetime.now() - datetime.timedelta(days=3, weeks=1)
#         LoginDay.objects.select_for_update().filter(pk=4).update(day=last_week1.date())

#         check_badge_conditions(user)
#         badge = Badge.objects.get(id_name="login-3")
#         earned = Earned.objects.filter(profile=user.profile, badge=badge)
#         self.assertEquals(len(earned), 1)

#     def test_award_consecutive_login_3_from_last_week_5(self):
#         user = User.objects.get(pk=1)
#         LoginDay.objects.create(profile=user.profile)
#         last_week3 = datetime.datetime.now() - datetime.timedelta(days=1, weeks=1)
#         LoginDay.objects.select_for_update().filter(pk=2).update(day=last_week3.date())

#         LoginDay.objects.create(profile=user.profile)
#         last_week2 = datetime.datetime.now() - datetime.timedelta(days=2, weeks=1)
#         LoginDay.objects.select_for_update().filter(pk=3).update(day=last_week2.date())

#         LoginDay.objects.create(profile=user.profile)
#         last_week1 = datetime.datetime.now() - datetime.timedelta(days=3, weeks=1)
#         LoginDay.objects.select_for_update().filter(pk=4).update(day=last_week1.date())

#         LoginDay.objects.create(profile=user.profile)
#         last_week4 = datetime.datetime.now() - datetime.timedelta(days=4, weeks=1)
#         LoginDay.objects.select_for_update().filter(pk=5).update(day=last_week4.date())

#         LoginDay.objects.create(profile=user.profile)
#         last_week5 = datetime.datetime.now() - datetime.timedelta(days=5, weeks=1)
#         LoginDay.objects.select_for_update().filter(pk=6).update(day=last_week5.date())

#         check_badge_conditions(user)
#         badge = Badge.objects.get(id_name="login-3")
#         earned = Earned.objects.filter(profile=user.profile, badge=badge)
#         self.assertEquals(len(earned), 1)

#     def test_no_award_consecutive_login_2_from_last_week(self):
#         user = User.objects.get(pk=1)
#         LoginDay.objects.create(profile=user.profile)
#         last_week3 = datetime.datetime.now() - datetime.timedelta(days=1, weeks=1)
#         LoginDay.objects.select_for_update().filter(pk=2).update(day=last_week3.date())

#         LoginDay.objects.create(profile=user.profile)
#         last_week2 = datetime.datetime.now() - datetime.timedelta(days=2, weeks=1)
#         LoginDay.objects.select_for_update().filter(pk=3).update(day=last_week2.date())

#         check_badge_conditions(user)
#         badge = Badge.objects.get(id_name="login-3")
#         earned = Earned.objects.filter(profile=user.profile, badge=badge)
#         self.assertEquals(len(earned), 0)

#     def test_award_solve_1_on_completed(self):
#         user = User.objects.get(pk=1)
#         question = Programming.objects.create(title="Test question", question_text="Print hello world")
#         attempt = Attempt.objects.create(profile=user.profile, question=question, passed_tests=True, is_save=False, user_code='')

#         check_badge_conditions(user)
#         badge = Badge.objects.get(id_name="solve-1")
#         earned = Earned.objects.filter(profile=user.profile, badge=badge)
#         self.assertEquals(len(earned), 1)

#     def test_not_award_solve_1_on_attempt(self):
#         user = User.objects.get(pk=1)
#         question = Programming.objects.create(title="Test question", question_text="Print hello world")
#         attempt = Attempt.objects.create(profile=user.profile, question=question, passed_tests=False, is_save=False, user_code='')

#         check_badge_conditions(user)
#         badge = Badge.objects.get(id_name="solve-1")
#         earned = Earned.objects.filter(profile=user.profile, badge=badge)
#         self.assertEquals(len(earned), 0)

# class BuggyQuestionViewTest(DjangoTestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # never modify this object in tests
#         User.objects.create_user(username='john', email='john@uclive.ac.nz', password='onion')
#         question = Buggy.objects.create(title="test", question_text="Print input", solution="i=input()\nprint(i)", buggy_program="i=input()\nprint(i[1:])")

#         token_file = open("../../token_file.txt", "r")
#         sphere_token = token_file.read().strip()
#         Token.objects.create(name='sphere', token=sphere_token)

#     def post_payload(self, url, payload):
#         resp = self.client.post(url, json.dumps(payload), content_type="application/json")
#         result = json.loads(resp.content.decode('utf-8'))
#         return result

#     def get_the_output(self, user_input, buggy_stdin, expected_print, expected_return, question_id, assertion):
#         payload = {
#             'user_input': user_input,
#             'buggy_stdin': buggy_stdin,
#             'expected_print': expected_print,
#             'expected_return': expected_return,
#             'question': question_id}
#         result = self.post_payload('/ajax/send_code/', payload)
#         self.assertIn('id', list(result.keys()))
#         submission_id = result['id']

#         payload = {'id': submission_id, 'question': question_id}
#         result = self.post_payload('/ajax/get_output/', payload)

#         if result['completed'] == False:
#             time.sleep(1)
#             result = self.post_payload('/ajax/get_output/', payload)
#             if result['completed'] == False:
#                 time.sleep(2)
#                 result = self.post_payload('/ajax/get_output/', payload)
#                 if result['completed'] == False:
#                     time.sleep(3)
#                     result = self.post_payload('/ajax/get_output/', payload)
#         #print(result['output'])
#         #print(result['stderr'])
#         #print(result['cmpinfo'])

#         self.assertTrue(result['completed'])
#         self.assertTrue(assertion in result['output'])

#     def test_buggy_program(self):
#         user_code = None
#         buggy_stdin = 'hello'
#         exp_print = 'hello\n'
#         exp_return = None

#         self.get_the_output(user_code, buggy_stdin, exp_print, exp_return, 1, '"correct": [true]')

#     def test_buggy_function(self):
#         BuggyFunction.objects.create(title="test", question_text="Print input", function_name="hi", solution="def hi(n):\n    return n", buggy_program="def hi(n):\n    return n+1")

#         user_code = '3'
#         buggy_stdin = ''
#         exp_print = ''
#         exp_return = '3'

#         self.get_the_output(user_code, buggy_stdin, exp_print, exp_return, 2, '"correct": [true]')

#     def test_buggy_function_and_input_output(self):
#         BuggyFunction.objects.create(title="test", question_text="Print input", function_name="hi", solution="def hi(n):\n    i=input()\n    print(i)\n    return n", buggy_program="def hi(n):\n    i=input()\n    print(i[1:])\n    return n")

#         user_code = '3'
#         buggy_stdin = 'hello'
#         exp_print = 'hello\n'
#         exp_return = '3'

#         self.get_the_output(user_code, buggy_stdin, exp_print, exp_return, 2, '"correct": [true]')

# class QuestionViewTest(DjangoTestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # never modify this object in tests
#         User.objects.create_user(username='john', email='john@uclive.ac.nz', password='onion')
#         question = Programming.objects.create(title="Test question", question_text="Print hello world")
#         TestCaseProgram.objects.create(question=question, expected_output="hello world\n")

#         token_file = open("../../token_file.txt", "r")
#         sphere_token = token_file.read().strip()
#         Token.objects.create(name='sphere', token=sphere_token)

#     def login_user(self):
#         login = self.client.login(username='john', password='onion')
#         self.assertTrue(login)

#     def post_payload(self, url, payload):
#         resp = self.client.post(url, json.dumps(payload), content_type="application/json")
#         result = json.loads(resp.content.decode('utf-8'))
#         return result

#     def get_the_output(self, user_code, question_id, assertion):
#         payload = {'user_input': user_code, 'question': question_id}
#         result = self.post_payload('/ajax/send_code/', payload)
#         self.assertIn('id', list(result.keys()))
#         submission_id = result['id']

#         payload = {'id': submission_id, 'question': question_id}
#         result = self.post_payload('/ajax/get_output/', payload)

#         if result['completed'] == False:
#             time.sleep(1)
#             result = self.post_payload('/ajax/get_output/', payload)
#             if result['completed'] == False:
#                 time.sleep(2)
#                 result = self.post_payload('/ajax/get_output/', payload)
#                 if result['completed'] == False:
#                     time.sleep(3)
#                     result = self.post_payload('/ajax/get_output/', payload)
#         print(result['output'])
#         print(result['stderr'])
#         print(result['cmpinfo'])

#         self.assertTrue(result['completed'])
#         self.assertTrue(assertion in result['output'])

#     ### tests begin ###

#     def test_url_exists_not_logged_in(self):
#         resp = self.client.get('/questions/1/')
#         self.assertEqual(resp.status_code, 200)

#     def test_url_exists_logged_in(self):
#         self.login_user()
#         resp = self.client.get('/questions/1/')
#         self.assertEqual(resp.status_code, 200)

#     def test_send_code(self):
#         user_code = 'print("hello world")'
#         payload = {'user_input': user_code, 'question': 1}
#         result = self.post_payload('/ajax/send_code/', payload)
#         self.assertIn('id', list(result.keys()))

#     def test_get_output_program(self):
#         user_code = 'print("hello world")'
#         self.get_the_output(user_code, 1, '"correct": [true]')

#     def test_get_output_program_multiple_test_cases(self):
#         question = Programming.objects.create(title="Test 2", question_text="Take off first char")
#         TestCaseProgram.objects.create(question=question, test_input="max", expected_output="ax\n")
#         TestCaseProgram.objects.create(question=question, test_input="seven", expected_output="even\n")

#         user_code = 't = input()\nprint(t[1:])'
#         self.get_the_output(user_code, 2, '"correct": [true, true]')

#     def test_get_output_program_blank_input(self):
#         question = Programming.objects.create(title="Test 2", question_text="Print input")
#         TestCaseProgram.objects.create(question=question, test_input="", expected_output="\n")

#         user_code = 't = input()\nprint(t)'
#         self.get_the_output(user_code, 2, '"correct": [true]')

#     def test_get_output_program_using_tab_to_indent(self):
#         question = Programming.objects.create(title="Test 2", question_text="Print hello")
#         TestCaseProgram.objects.create(question=question, expected_output="hello\n")

#         user_code = 'if True:\n\tprint("hello")'
#         self.get_the_output(user_code, 2, '"correct": [true]')

#     def test_get_output_program_using_spaces_to_indent(self):
#         question = Programming.objects.create(title="Test 2", question_text="Print hello")
#         TestCaseProgram.objects.create(question=question, expected_output="hello\n")

#         user_code = 'if True:\n    print("hello")'
#         self.get_the_output(user_code, 2, '"correct": [true]')

#     def test_get_output_program_escaped_newline_not_replaced(self):
#         question = Programming.objects.create(title="Test 2", question_text="Print hello world on different lines using single print")
#         TestCaseProgram.objects.create(question=question, expected_output="hello\nworld\n")

#         user_code = 'print("hello\\nworld")'
#         self.get_the_output(user_code, 2, '"correct": [true]')

#     # functions

#     def test_get_output_function(self):
#         question = ProgrammingFunction.objects.create(title="Test 2", question_text="Return given word", function_name="direct_return")
#         TestCaseFunction.objects.create(question=question, function_params="'hello'", expected_return="'hello'")

#         user_code = 'def direct_return(word):\n    return word'
#         self.get_the_output(user_code, 2, '"correct": [true]')

#     def test_get_output_print_function(self):
#         question = ProgrammingFunction.objects.create(title="Test 2", question_text="Print given word", function_name="direct_print")
#         TestCaseFunction.objects.create(question=question, function_params="'hello'", expected_output="hello\n", expected_return="")

#         user_code = 'def direct_print(word):\n    print(word)'
#         self.get_the_output(user_code, 2, '"correct": [true]')

#     def test_get_output_print_and_return_function_multiple_test_cases(self):
#         question = ProgrammingFunction.objects.create(title="Test 2", question_text="Print and return given word", function_name="print_return")
#         TestCaseFunction.objects.create(question=question, function_params="'hello'", expected_output="hello\n", expected_return="'hello'")
#         TestCaseFunction.objects.create(question=question, function_params="'world'", expected_output="world\n", expected_return="'world'")

#         user_code = 'def print_return(word):\n    print(word)\n    return word'
#         self.get_the_output(user_code, 2, '"correct": [true, true]')

#     def test_blank_test_function_multiple_test_cases(self):
#         question = ProgrammingFunction.objects.create(title="Test 2", question_text="Return the string doubled", function_name="return_double")
#         TestCaseFunction.objects.create(question=question, function_params="'hello'", expected_return="'hellohello'")
#         TestCaseFunction.objects.create(question=question, function_params="''", expected_return="''")

#         user_code = 'def return_double(word):\n    return word + word'
#         self.get_the_output(user_code, 2, '"correct": [true, true]')

#     def test_function_multiple_params(self):
#         question = ProgrammingFunction.objects.create(title="Test 2", question_text="Add the strings", function_name="add_words")
#         TestCaseFunction.objects.create(question=question, function_params="'good','night'", expected_return="'goodnight'")

#         user_code = 'def add_words(word1, word2):\n    return word1 + word2'
#         self.get_the_output(user_code, 2, '"correct": [true]')

#     def test_function_false_for_incorrect_answer(self):
#         question = ProgrammingFunction.objects.create(title="Test 2", question_text="Add the strings", function_name="add_words")
#         TestCaseFunction.objects.create(question=question, function_params="'good','night'", expected_return="'goodnight'")

#         user_code = 'def add_words(word1, word2):\n    return word1'
#         self.get_the_output(user_code, 2, '"correct": [false]')
