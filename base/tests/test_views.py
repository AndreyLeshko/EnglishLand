from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class MainPageTest(TestCase):

    def test_response_by_url(self):
        url = '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_response_by_path_name(self):
        url = reverse('base:main_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TrainerPageNotAuthorizedTestCase(TestCase):

    def test_response_by_url(self):
        url = '/trainer/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_response_by_path_name(self):
        url = reverse('base:trainer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class TrainerPageAuthorizedTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='Alexey', email='alexey@mail.ru', password='Alexey123')
        self.client.login(username='Alexey', password='Alexey123')

    def test_response_by_url(self):
        url = '/trainer/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_response_by_path_name(self):
        url = reverse('base:trainer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
