from django.urls import reverse  # type: ignore
import pytest  # type: ignore

from parameterized import parameterized  # type: ignore

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


from .base import AuthorsBaseTest

# CLASS to Register Form Functional tests


@pytest.mark.functionaltest
class AuthorsRegisterFunctionalTest(AuthorsBaseTest):

    # Method to fill the form with spaces
    # The e-mail is different because the form requires a valid
    # one to submit the form.
    # Inserting an invalid e-mail prevent the form submission
    def fill_form_with_dummy_data(self, form, email='email@server.com'):

        # Getting the input fields from the form
        fields = form.find_elements(By.TAG_NAME, 'input')

        # Looping through the fields.
        # If the field is the e-mail, send the e-mail value
        # if not, send 8 ' '
        for field in fields:
            # If statement to avoid the hidden input created
            # by the csrf_token
            if field.is_displayed():
                if field.accessible_name == 'E-mail':
                    field.send_keys(email)
                else:
                    field.send_keys(' ' * 8)

    # Method to get the form that will be require by the tests
    def get_form(self):
        # Uses the webdriver (self.browser) to find the register form
        # using its XPATH
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form')

    # Method with callback.
    def form_fill_with_callback(self, callback):
        # Get the page
        self.browser.get(self.live_server_url + '/authors/register/')

        # Get the desired form in the page
        form = self.get_form()

        # Fill the form with dummy data
        self.fill_form_with_dummy_data(form)

        # Call back the method received as argument
        callback(form)

        return form

    # TEST if the empty fields fired errors
    @parameterized.expand([
        ('first_name', 'The first name must not be empty.'),
        ('last_name', 'The last name must not be empty.'),
        ('username', 'The username is required.'),
        ('password', 'The password is required.'),
        ('password2', 'The confirmation password is required.'),
    ])
    def test_fields_are_required(self, field, error_message):

        def callback(form):
            # Sending the form using ENTER
            self.get_by_id(form, 'id_first_name').send_keys(Keys.ENTER)

            # waiting the new page to load
            self.sleep(1)

            # Getting the form again. The page was reloaded
            # register -> register_create -> register
            # and the previous form is not accessible anymore
            form = self.get_form()

            # Assertions:
            # Check if the error message is displayed in the form to each field
            self.assertIn(
                error_message,
                form.text,
                msg="AUTHORS:REGISTER - EMPTY FIELD: An empty field was "
                f"allowed. Field: {field}")

        self.form_fill_with_callback(callback)

    # TEST if the error message to wrong password confirmation value
    def test_passwords_do_not_match_error(self):
        # Method to be passed as callback to the
        # method form_fill_with_callback()
        def callback(form):
            # Inserting different values to password and password confirmation
            self.get_by_id(form, 'id_password').send_keys('Password')
            self.get_by_id(form, 'id_password2').send_keys('Password2')

            # Sending enter to submit the form
            self.get_by_id(form, 'id_password').send_keys(Keys.ENTER)

            # Waiting a while to load the page
            self.sleep(1)

            # Getting the form again (because the page reloaded)
            form = self.get_form()

            # Assertions:
            # Check if the error message was found in the form
            self.assertIn(
                'The passwords must be equal.',
                form.text,
                msg="AUTHORS:REGISTER - PASSWORD CONFIRMATION: The passwords "
                "were not confirmed. The error message was not displayed"
                ", although it was expected."
            )

        self.form_fill_with_callback(callback)

    # TEST if valid user can be register
    def test_user_valid_data_register_success(self):
        # Getting the register page
        self.browser.get(self.live_server_url + '/authors/register/')

        # Getting the form in the page and filling each field with valid data
        form = self.get_form()
        self.get_by_id(form, 'id_first_name').send_keys('FirstName')
        self.get_by_id(form, 'id_last_name').send_keys('LastName')
        self.get_by_id(form, 'id_username').send_keys('UserName123')
        self.get_by_id(form, 'id_email').send_keys('myemail@server.com')
        self.get_by_id(form, 'id_password').send_keys('Password1234')
        self.get_by_id(form, 'id_password2').send_keys('Password1234')

        # Submitting the form
        form.submit()

        # waiting the page to reload
        self.sleep(1)

        # Assertions:
        # Check if the success message was found in the body tag
        self.assertIn(
            "Your user was created. Please, log in",
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="AUTHORS:REGISTER - VALID USER INSERTION: Valid user data "
                "was NOT accepted as valid. Success message wasn't found. "
        )

    def test_user_email_must_be_unique(self):
        for i in range(2):
            # Getting the register page
            self.browser.get(self.live_server_url + '/authors/register/')

            # Getting the form in the page and filling each field with
            # valid data
            form = self.get_form()
            self.get_by_id(form, 'id_first_name').send_keys('FirstName')
            self.get_by_id(form, 'id_last_name').send_keys('LastName')
            self.get_by_id(form, 'id_username').send_keys(f'UserName123{i}')
            self.get_by_id(form, 'id_email').send_keys('myemail@server.com')
            self.get_by_id(form, 'id_password').send_keys('Password1234')
            self.get_by_id(form, 'id_password2').send_keys('Password1234')

            # Submitting the form
            form.submit()

            # waiting the page to reload
            self.sleep(1)

        # Assertions:
        # Check if the success message was found in the body tag
        self.assertIn(
            "This e-mail is already in use.",
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="AUTHORS:REGISTER - UNIQUE E-MAIL REQUIRED: A non unique email"
                " was accepted. Error message not found. "
        )

    # TEST if register view returns 404 if user tries to GET
    # the register_create
    def test_authors_register_view_returns_404_to_GET(self):
        # GET the register_create view.
        # Expecting receive 404 page
        self.browser.get(
            self.live_server_url +
            reverse('authors:register_create'))

        # Assertions:
        # Checking if the Not Found message was found in the page
        # displayed to the user
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text,
            msg="REGISTER_CREATE - GET METHOD: The GET register_create did NOT"
            " return 404 page. 'Not Found' message not found"
        )
