from django.test import TestCase
from style.models import Error


class TopicModelTest(TestCase):

    def test_error_str(self):
        error = Error(
            language='lang',
            code='code123',
        )
        error.save()
        self.assertEqual(error.__str__(), "lang - code123")
