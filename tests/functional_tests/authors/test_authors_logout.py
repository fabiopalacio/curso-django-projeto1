
import time
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
import pytest
from utils.browser import make_firefox_browser
from selenium.webdriver.common.by import By

# pytest to mark this as functionaltest


@pytest.mark.functionaltest
# CLASS to test logout functionalities
# It requires the user to be logged in
class AuthorsLogoutTest(LiveServerTestCase):
    # setup method:
    #   1) Create the browser
    #   2) Create an user and save its password to self.password variable
    def setUp(self) -> None:
        # Create the browser:
        # It calls the the util method to create the browser.
        self.browser = make_firefox_browser()

        # Saving the password. The create_user() method protect the password,
        #   making the self.my_user.password not usable to login
        self.password = 'my_password'

        # Creating the user with the password above
        self.my_user = User.objects.create_user(
            username='my_user', password=self.password)

        return super().setUp()

    # tearDown method.
    #   1) Quit the browser
    #   2) Deleting all users.
    def tearDown(self) -> None:
        # Quit the browser.
        self.browser.quit()

        # Deleting all users. Used to avoid problems between tests
        users = User.objects.all()
        users.delete()

        return super().tearDown()

    # Method sleep to wait page to load
    def sleep(self, qty=1):
        time.sleep(qty)

    # Method to login. The logout functionalities require user to be
    # logged in.
    def login(self):
        # Get the browser to access the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Finding the login form by its class.
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Finding the username and password fields and inserting the
        # user's username and password. The password used is the stored
        # in self.password
        username_field = form.find_element(By.ID, 'id_username')
        username_field.send_keys(self.my_user.username)
        password_field = form.find_element(By.ID, 'id_password')
        password_field.send_keys(self.password)

        # Submiting the form to login
        form.submit()

    # TEST if an user can logout
    def test_authors_logout_works(self):

        # User login
        self.login()
        # Wait a while to page load
        self.sleep(1)

        # For the purpose of this test, we need the button element
        # to logout and click in it
        logout_button = self.browser.find_element(
            By.CLASS_NAME, 'logout-button')
        logout_button.click()

        # Wait a while to page load
        self.sleep(1)

        # Assertions:
        # Check if the logout was succesfully made.
        # The test check if the success message is displayed to the user
        # in the new page
        self.assertIn(
            'Logout successfully',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg='DASHBOARD LOGOUT - SUCCESS MESSAGE: Sucess message not found.'
        )
