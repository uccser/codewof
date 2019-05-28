# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time

# from questions.models import *

# class QuestionTestCase(StaticLiveServerTestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = webdriver.Firefox()
#         cls.selenium.implicitly_wait(10)

#         question = Programming.objects.create(title="Test question", question_text="Print hello world")
#         TestCaseProgram.objects.create(question=question, expected_output="hello world\n")

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()

#     ### tests begin ###

#     def test_random_question_button(self):
#         selenium = self.selenium
#         selenium.get(self.live_server_url)
#         random_question_button = selenium.find_element_by_link_text('Random Question')
#         random_question_button.click()
#         assert 'Test question' in selenium.page_source


# class SignUpTestCase(StaticLiveServerTestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = webdriver.Firefox()
#         cls.selenium.implicitly_wait(10)

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()

#     ### tests begin ###

#     def test_register_blue_sky(self):
#         selenium = self.selenium
#         selenium.get(self.live_server_url)
#         sign_up_button = selenium.find_element_by_link_text('Sign Up')
#         sign_up_button.click()

#         username = selenium.find_element_by_id('id_username')
#         first_name = selenium.find_element_by_id('id_first_name')
#         last_name = selenium.find_element_by_id('id_last_name')
#         email = selenium.find_element_by_id('id_email')
#         password1 = selenium.find_element_by_id('id_password1')
#         password2 = selenium.find_element_by_id('id_password2')

#         submit = selenium.find_element_by_id('sign_up_button')

#         username.send_keys('wizard')
#         email.send_keys('ur-a-wizard@uclive.ac.nz')
#         password1.send_keys('harrypotter')
#         password2.send_keys('harrypotter')

#         submit.send_keys(Keys.RETURN)
#         time.sleep(5)
#         assert 'Prototype 402' in selenium.title

#     def test_register_bad_password(self):
#         selenium = self.selenium
#         selenium.get(self.live_server_url)
#         sign_up_button = selenium.find_element_by_link_text('Sign Up')
#         sign_up_button.click()

#         username = selenium.find_element_by_id('id_username')
#         first_name = selenium.find_element_by_id('id_first_name')
#         last_name = selenium.find_element_by_id('id_last_name')
#         email = selenium.find_element_by_id('id_email')
#         password1 = selenium.find_element_by_id('id_password1')
#         password2 = selenium.find_element_by_id('id_password2')

#         submit = selenium.find_element_by_id('sign_up_button')

#         username.send_keys('wizard')
#         last_name.send_keys('Potter')
#         email.send_keys('ur-a-wizard@uclive.ac.nz')
#         password1.send_keys('harrypotter')
#         password2.send_keys('harrypotter')

#         time.sleep(1)
#         submit.send_keys(Keys.RETURN)
#         time.sleep(1)
#         assert 'too similar to the last name' in selenium.page_source
