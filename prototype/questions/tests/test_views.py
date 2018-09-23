# from django.test import TestCase as DjangoTestCase
# from django.contrib.auth.models import User
# from django.contrib.auth import login
# from unittest import skip
# import json
# import time

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

# class QuestionViewTest(DjangoTestCase):
#     @classmethod
#     def setUpTestData(cls):
#         User.objects.create_user(username='john', email='john@uclive.ac.nz', password='onion')
#         TestCase.objects.create(expected_output="hello world\\n")
#         program = QuestionType.objects.create(name="Program")
#         question = Question.objects.create(title="Test question", question_text="Print hello world", question_type=program)
#         question.test_cases.add(1)
#         question.save()

#         token_file = open("../../token_file.txt", "r")
#         sphere_token = token_file.read().strip()
#         Token.objects.create(name='sphere', token=sphere_token)

#     def login_user(self):
#         login = self.client.login(username='john', password='onion')
#         self.assertTrue(login)

#     def get_the_output(self, user_code, question_id, assertion):
#         payload = {'user_input': user_code, 'question': question_id}
#         resp = self.client.post('/ajax/send_code/', payload)
#         result = json.loads(resp.content.decode('utf-8'))
#         self.assertIn('id', list(result.keys()))
#         submission_id = result['id']

#         payload = {'id': submission_id, 'question': question_id}
#         resp = self.client.post('/ajax/get_output/', payload)
#         result = json.loads(resp.content.decode('utf-8'))

#         if result['completed'] == False:
#             time.sleep(1)
#             resp = self.client.post('/ajax/get_output/', payload)
#             result = json.loads(resp.content.decode('utf-8'))
#             if result['completed'] == False:
#                 time.sleep(2)
#                 resp = self.client.post('/ajax/get_output/', payload)
#                 result = json.loads(resp.content.decode('utf-8'))
#                 if result['completed'] == False:
#                     time.sleep(3)
#                     resp = self.client.post('/ajax/get_output/', payload)
#                     result = json.loads(resp.content.decode('utf-8'))
        
#         self.assertTrue(result['completed'])
#         print(result['output'])
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
#         resp = self.client.post('/ajax/send_code/', payload)
#         result = json.loads(resp.content.decode('utf-8'))
#         self.assertIn('id', list(result.keys()))
#         submission_id = result['id']
#         return submission_id
    
#     def test_get_output_program(self):
#         user_code = 'print("hello world")'
#         self.get_the_output(user_code, 1, '"correct": [true]')


#     def test_get_output_program_multiple_test_cases(self):
#         TestCase.objects.create(test_input="max", expected_output="ax\\n")
#         TestCase.objects.create(test_input="seven", expected_output="even\\n")
#         program = QuestionType.objects.create(name="Program")
#         question = Question.objects.create(title="Test 2", question_text="Take off first char", question_type=program)
#         question.test_cases.add(2)
#         question.test_cases.add(3)
#         question.save()

#         user_code = 't = input()\nprint(t[1:])'
#         self.get_the_output(user_code, 2, '"correct": [true, true]')

#     def test_get_output_program_blank_input(self):
#         TestCase.objects.create(test_input="", expected_output="\\n")
#         program = QuestionType.objects.create(name="Program")
#         question = Question.objects.create(title="Test 2", question_text="Print input", question_type=program)
#         question.test_cases.add(2)
#         question.save()

#         user_code = 't = input()\nprint(t)'
#         self.get_the_output(user_code, 2, '"correct": [true]')
        
#     def test_get_output_function(self):
#         TestCase.objects.create(function_params="hello", expected_return="hello")
#         function = QuestionType.objects.create(name="Function")
#         question = Question.objects.create(title="Test 2", question_text="Return given word", question_type=function, function_name="direct_return")
#         question.test_cases.add(2)
#         question.save()

#         user_code = 'def direct_return(word):\n    return word'
#         self.get_the_output(user_code, 2, '"correct": [true]')

#     def test_get_output_print_function(self):
#         TestCase.objects.create(function_params="hello", expected_output="hello\\n")
#         function = QuestionType.objects.create(name="Function")
#         question = Question.objects.create(title="Test 2", question_text="Print given word", question_type=function, function_name="direct_print")
#         question.test_cases.add(2)
#         question.save()

#         user_code = 'def direct_print(word):\n    print(word)'
#         self.get_the_output(user_code, 2, '"correct": [true]')

#     def test_get_output_print_and_return_function_multiple_test_cases(self):
#         TestCase.objects.create(function_params="hello", expected_output="hello\\n", expected_return="hello")
#         TestCase.objects.create(function_params="world", expected_output="world\\n", expected_return="world")
#         function = QuestionType.objects.create(name="Function")
#         question = Question.objects.create(title="Test 2", question_text="Print and return given word", question_type=function, function_name="print_return")
#         question.test_cases.add(2)
#         question.test_cases.add(3)
#         question.save()

#         user_code = 'def print_return(word):\n    print(word)\n    return word'
#         self.get_the_output(user_code, 2, '"correct": [true, true]')

#     def test_blank_test_function_multiple_test_cases(self):
#         TestCase.objects.create(function_params="hello", expected_return="hellohello")
#         TestCase.objects.create(function_params="", expected_return="")
#         function = QuestionType.objects.create(name="Function")
#         question = Question.objects.create(title="Test 2", question_text="Return the string doubled", question_type=function, function_name="return_double")
#         question.test_cases.add(2)
#         question.test_cases.add(3)
#         question.save()

#         user_code = 'def return_double(word):\n    return word + word'
#         self.get_the_output(user_code, 2, '"correct": [true, true]')

#     def test_function_multiple_params(self):
#         TestCase.objects.create(function_params="good,night", expected_return="goodnight")
#         function = QuestionType.objects.create(name="Function")
#         question = Question.objects.create(title="Test 2", question_text="Add the strings", question_type=function, function_name="add_words")
#         question.test_cases.add(2)
#         question.save()

#         user_code = 'def add_words(word1, word2):\n    return word1 + word2'
#         self.get_the_output(user_code, 2, '"correct": [true]')

#     def test_function_false_for_incorrect_answer(self):
#         TestCase.objects.create(function_params="good,night", expected_return="goodnight")
#         function = QuestionType.objects.create(name="Function")
#         question = Question.objects.create(title="Test 2", question_text="Add the strings", question_type=function, function_name="add_words")
#         question.test_cases.add(2)
#         question.save()

#         user_code = 'def add_words(word1, word2):\n    return word1'
#         self.get_the_output(user_code, 2, '"correct": [false]')


