from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorsLogoutTest(TestCase):
    def test_user_tries_to_logout_by_get_method(self):

        User.objects.create_user(username='my_user', password='my_password')
        self.client.login(username='my_user', password='my_password')

        url = reverse('authors:logout')
        response = self.client.get(url, follow=True)

        self.assertIn(
            'Invalid logout request',
            response.content.decode('utf-8'),
            msg=" Error"
        )

    def test_user_tries_to_logout_another_user(self):

        User.objects.create_user(username='my_user', password='my_password')
        self.client.login(username='my_user', password='my_password')

        url = reverse('authors:logout')
        response = self.client.post(
            url,
            data={'username': 'another_user', 'password': 'my_password'},
            follow=True)

        self.assertIn(
            'Invalid username',
            response.content.decode('utf-8'),
            msg=" Error"
        )

    def test_user_logout_successfully(self):

        User.objects.create_user(username='my_user', password='my_password')
        self.client.login(username='my_user', password='my_password')

        url = reverse('authors:logout')
        response = self.client.post(
            url,
            data={'username': 'my_user'},
            follow=True)

        self.assertIn(
            'Logout successfully',
            response.content.decode('utf-8'),
            msg=" Error"
        )
