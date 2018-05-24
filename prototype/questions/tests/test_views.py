from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import login
from unittest import skip

from questions.models import Profile
from questions.views import ProfileView


class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # never modify this object in tests
        user = User.objects.create_user(username='john', email='john@uclive.ac.nz', password='onion')
        pass
    
    def setUp(self):
        pass

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/profile/')
        self.assertRedirects(resp, '/login/?next=/profile/')

    def test_view_url_exists(self):
        user = User.objects.get(id=1)
        login = self.client.login(username='john', password='onion')
        self.assertTrue(login)
        resp = self.client.get('/profile/')
        self.assertEqual(resp.status_code, 200)
    
    def test_view_uses_correct_template(self):
        user = User.objects.get(id=1)
        login = self.client.login(username='john', password='onion')
        self.assertTrue(login)
        resp = self.client.get('/profile/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/profile.html')