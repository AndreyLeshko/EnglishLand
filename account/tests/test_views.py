from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from account.models import Profile


class PersonalPageNotAuthorizedTestCase(TestCase):

    def test_response_by_url(self):
        url = '/accounts/profile/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_response_code_by_path_name(self):
        url = reverse('account:personal_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class PersonalPageAuthorizedTestCase(TestCase):

    def setUp(self):
        user = User.objects.get_or_create(username='Alexey', email='alexey@mail.ru')[0]
        user.set_password('Alexey123')
        user.save()
        self.client.login(username='Alexey', password='Alexey123')

    def test_response_by_url(self):
        url = '/accounts/profile/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_response_by_path_name(self):
        url = reverse('account:personal_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class RegisterPageTestCase(TestCase):

    def test_response_by_url(self):
        url = '/accounts/register/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_response_by_path_name(self):
        url = reverse('account:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class EditProfilePageNotAuthorizedTestCase(TestCase):

    def test_response_by_url(self):
        url = '/accounts/edit/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_response_code_by_path_name(self):
        url = reverse('account:edit')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class EditProfilePageAuthorizedTestCase(TestCase):

    def setUp(self):
        user = User.objects.get_or_create(username='Alexey', email='alexey@mail.ru')[0]
        user.set_password('Alexey123')
        user.save()
        Profile.objects.create(user=user, date_of_birth='1880-12-12')
        self.client.login(username='Alexey', password='Alexey123')

    def test_response_by_url(self):
        url = '/accounts/edit/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_response_by_path_name(self):
        url = reverse('account:edit')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class LoginPageTestCase(TestCase):

    def test_response_by_url(self):
        url = '/accounts/login/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_response_by_path_name(self):
        url = reverse('account:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class LogoutPageTestCase(TestCase):

    def test_response_by_url(self):
        url = '/accounts/logout/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_response_by_path_name(self):
        url = reverse('account:logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class PasswordChangePageNotAuthorizedTestCase(TestCase):

    def test_response_by_url(self):
        url = '/accounts/password-change/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_response_by_path_name(self):
        url = reverse('account:password_change')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class PasswordChangePageAuthorizedTestCase(TestCase):

    def setUp(self):
        user = User.objects.get_or_create(username='Alexey', email='alexey@mail.ru')[0]
        user.set_password('Alexey123')
        user.save()
        self.client.login(username='Alexey', password='Alexey123')

    def test_response_by_url(self):
        url = '/accounts/password-change/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_response_by_path_name(self):
        url = reverse('account:password_change')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class PasswordChangeDonePageNotAuthorizedTestCase(TestCase):

    def test_response_by_url(self):
        url = '/accounts/password-change/done/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_response_by_path_name(self):
        url = reverse('account:password_change_done')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class PasswordChangeDonePageAuthorizedTestCase(TestCase):

    def setUp(self):
        user = User.objects.get_or_create(username='Alexey', email='alexey@mail.ru')[0]
        user.set_password('Alexey123')
        user.save()
        self.client.login(username='Alexey', password='Alexey123')

    def test_response_by_url(self):
        url = '/accounts/password-change/done/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_response_by_path_name(self):
        url = reverse('account:password_change_done')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class PasswordResetPageTestCase(TestCase):

    def test_response_by_url(self):
        url = '/accounts/password-reset/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_response_by_path_name(self):
        url = reverse('account:password_reset')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class PasswordResetDonePageTestCase(TestCase):

    def test_response_by_url(self):
        url = '/accounts/password-reset/done/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_response_by_path_name(self):
        url = reverse('account:password_reset_done')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
