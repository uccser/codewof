from django.test import SimpleTestCase, TestCase

from questions.forms import SignUpForm

class SignUpFormTest(SimpleTestCase):

    def test_email_help_text(self):
        form = SignUpForm()
        expected = 'Please enter a valid email address'
        self.assertEqual(form.fields['email'].help_text, expected)
