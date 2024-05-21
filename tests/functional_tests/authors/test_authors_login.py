from django.urls import reverse
import pytest
from django.contrib.auth.models import User

from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functionaltest
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'MyPassword1234'

        user = User.objects.create_user(
            username='my_user',
            password=string_password)

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_field = form.find_element(By.ID, 'id_username')
        username_field.send_keys(user.username)

        password_field = form.find_element(By.ID, 'id_password')
        password_field.send_keys(string_password)

        form.submit()
        self.sleep(1)

        self.assertIn(
            'You are logged in.',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="AUTHORS:LOGIN - VALID USER: User wasn't accepted to log in "
            "with valid data. Success message wasn't found in the body.")

    def test_get_login_auth_view_returns_404(self):

        self.browser.get(self.live_server_url + reverse('authors:login_auth'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg='Deu Ruim'
        )
