
from django.test import TestCase
from django.urls import reverse

# CLASS to test login View


class LoginViewTest(TestCase):
    # TEST if login_auth returns 404  to GET method
    def test_login_view_returns_404(self):
        # Getting the url to login_auth
        url = reverse('authors:login_auth')

        # Getting the response to GET the url
        response = self.client.get(url)

        # Assertions:
        # Check the status code returned
        self.assertEqual(
            404,
            response.status_code,
            msg="AUTHORS LOGIN_AUTH VIEW - GET VIEW: Get request did NOT "
            "returned 404 status code. Expected code: 404. Found: "
            f"{response.status_code}")

    # TEST if view return error message to invalid form

    def test_login_view_invalid_form_return_error_message(self):
        # Creating invalid form with no username inserted
        form_data = {'username': '', 'password': 'Password123'}

        # Posting the form to the view and saving it response.
        response = self.client.post(
            '/authors/login/auth/', form_data, follow=True)

        # Assertions:
        # Checking if the error message was displayed to the user
        self.assertIn(
            'class="message message-error">\n                '
            'Invalid credentials.',
            response.content.decode('utf-8'),
            msg='LOGIN_AUTH - CREDENTIALS: Expected error message after '
            'inserting invalid credentials.'
        )

    # TEST if the view returns a warning message to unauthenticated user
    def test_login_view_unauthenticate_form_return_warning(self):
        # Creating a valid form, but invalid user
        form_data = {'username': '123456', 'password': 'Password123'}

        # Posting the form and saving the response
        response = self.client.post(
            '/authors/login/auth/', form_data, follow=True)

        # Assertios:
        # Check if the WARNING message was displayed to the user
        self.assertIn(
            'class="message message-warning">\n                '
            'Invalid credentials.',
            response.content.decode('utf-8'),
            msg='LOGIN_AUTH - CREDENTIALS: Expected warning message after '
            'inserting invalid credentials.'
        )
