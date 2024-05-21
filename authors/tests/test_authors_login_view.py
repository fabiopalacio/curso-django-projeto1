
from django.test import TestCase
from django.urls import reverse


class LoginViewTest(TestCase):
    def test_login_view_returns_404(self):
        url = reverse('authors:login_auth')
        response = self.client.get(url)
        self.assertEqual(
            404,
            response.status_code,
            msg="AUTHORS LOGIN_AUTH VIEW - GET VIEW: Get request did NOT "
            "returned 404 status code. Expected code: 404. Found: "
            f"{response.status_code}")
