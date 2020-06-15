from django.test import TestCase
from django.urls import reverse


class HomeURLTest(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = "en"

    def test_home_url(self):
        url = reverse("style:home")
        self.assertEqual(url, "/style/")
