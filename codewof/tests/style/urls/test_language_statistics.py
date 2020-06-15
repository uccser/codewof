from django.test import TestCase
from django.urls import reverse


class LanguageStatisticsURLTest(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"

    def test_language_url(self):
        kwargs = {
            "language": "lang"
        }
        url = reverse("style:language_statistics", kwargs=kwargs)
        self.assertEqual(url, "/style/lang/statistics/")
