from django.urls import reverse
import pytest
from django.contrib.auth.models import User

from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest

# CLASS to functional tests to login views


@pytest.mark.functionaltest
class AuthorsLoginTest(AuthorsBaseTest):

    # Test if a valid user can login
    def test_user_valid_data_can_login_successfully(self):

        # Saving the password to be used in multiple points
        # in this test
        string_password = 'MyPassword1234'

        # Creating an user
        user = User.objects.create_user(
            username='my_user',
            password=string_password)

        # Acessing the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Getting the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Inserting the username and password
        username_field = form.find_element(By.ID, 'id_username')
        username_field.send_keys(user.username)

        password_field = form.find_element(By.ID, 'id_password')
        password_field.send_keys(string_password)

        # Submitting the form
        form.submit()

        # Waiting the page to load
        self.sleep(1)

        # Assertions:
        # Check if the successfull login message was displayed to the user
        self.assertIn(
            'You are logged in.',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="AUTHORS:LOGIN - VALID USER: User wasn't accepted to log in "
            "with valid data. Success message wasn't found in the body.")

    # TEST if GET method to login_auth returns 404
    def test_get_login_auth_view_returns_404(self):

        # Getting the page
        self.browser.get(self.live_server_url + reverse('authors:login_auth'))

        # Assertions:
        # Check if Not Found message was found in the returned page.
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg='Deu Ruim'
        )

    # TEST if an invalid form returns an error message
    def test_login_auth_error_message_to_invalid_form(self):
        # Accessing the page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Getting the form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Inserting only space in username
        # This makes the form invalid
        username_field = self.get_by_id(form, 'id_username')
        password_field = self.get_by_id(form, 'id_password')

        username_field.send_keys(' ')
        password_field.send_keys('Apassword123')

        # Submitting the form
        form.submit()

        # Waiting the page reload
        self.sleep(1)

        # Assertions:
        # Check if the "Invalid credentials." was displayed as an error
        # message to the user
        self.assertIn(
            'Invalid credentials.',
            self.browser.find_element(By.CLASS_NAME, 'message-error').text,
            msg="AUTHORS:LOGIN - CREDENTIALS: Error message to invalid "
            "credentials not found"
        )

    # TEST if an unauthenticated user returns warning message
    def test_login_auth_warning_message_to_invalid_user(self):
        # Accessing the page
        self.browser.get(self.live_server_url + reverse('authors:login'))
        # Getting the form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Inserting username and password valids, but not
        # registered.
        username_field = self.get_by_id(form, 'id_username')
        password_field = self.get_by_id(form, 'id_password')

        username_field.send_keys('123username')
        password_field.send_keys('Apassword123')

        # Submitting the form
        form.submit()

        # Waiting the page reload
        self.sleep(1)

        # Assertions:
        # Check if the "Invalid credentials." was displayed as warning
        # message to the user
        self.assertIn(
            'Invalid credentials.',
            self.browser.find_element(By.CLASS_NAME, 'message-warning').text,
            msg="AUTHORS:LOGIN - CREDENTIALS: Warning message to invalid "
            "credentials not found"
        )
