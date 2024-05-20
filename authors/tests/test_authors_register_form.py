from django.urls import reverse  # type: ignore
from django.test import TestCase as DjangoTestCase  # type: ignore

from unittest import TestCase
from parameterized import parameterized  # type: ignore

from authors.forms import RegisterForm

# Class to the Unit tests to the authors app


class AuthorsRegisterFormUnitTest(TestCase):

    # Test to check if the correct placeholder is in the form
    # Using parameterized to run subtests
    @parameterized.expand([
        ('first_name', 'Your first name'),
        ('last_name', 'Your last name'),
        ('email', 'Your e-mail'),
        ('username', 'Your username'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password')
    ])
    def test_field_placeholder_is_correct(self, field, exp_placeholder):

        # Creating a form object
        form = RegisterForm()

        # Getting the placeholder from the form for each field
        placeholder = form[field].field.widget.attrs['placeholder']

        # Assertions:
        # Check if the placeholder available in the parameterized above
        # was found in the form
        self.assertEqual(
            placeholder, exp_placeholder,
            msg=f"The {field}'s placeholder is incorrect")

    # TEST to check if the correct help text is in the form
    # Using parameterized to run subtests
    @parameterized.expand([
        ('username', 'Required. Length between 4 and 150 characters. Accepts '
         'uppercase and lowercase letters, numbers, and special characters.'),
        (
            'password',
            ('Password must have at least one uppercase letter, '
             'one lowercase and one number. The length '
             'should be at least 8 characters.')),
    ])
    def test_field_help_text_is_correct(self, field, exp_help_text):

        # Creating a form object
        form = RegisterForm()

        # Getting the help text from the form for each field
        help_text = form[field].field.help_text

        # Assertions:
        # Check if the help text available in the parameterized above
        # was found in the form
        self.assertEqual(
            help_text, exp_help_text,
            msg=f"The {field}'s help text is incorrect")

    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('email', 'E-mail'),
        ('username', 'Username'),
        ('password', 'Password'),
        ('password2', 'Repeat your password')
    ])
    def test_field_label_is_correct(self, field, exp_label):
        form = RegisterForm()
        label = form[field].field.label
        self.assertEqual(
            label, exp_label,
            msg=f"The {field}'s label is incorrect")


# Class to the integration tests to the authors app
class AuthorsRegisterFormIntegrationTest(DjangoTestCase):

    # SetUp: It runs before each individual test
    def setUp(self, *args, **kwargs) -> None:
        # Creating a dictionary with form informations to be used
        # in the tests
        # All values in this setup are valid.
        self.form_data = {
            'username': 'User',
            'first_name': 'John',
            'last_name': 'Silva',
            'email': 'john@mail.com',
            'password':  'Str0ngPassword',
            'password2': 'Str0ngPassword'
        }

        return super().setUp(*args, **kwargs)

    # TEST to check if the form captures the empty fields
    # and return a error message
    # Using Parameterized to run subtests.
    @parameterized.expand([
        ('username', 'The username is required.'),
        ('first_name', 'The first name must not be empty.'),
        ('last_name', 'The last name must not be empty.'),
        ('email', 'The e-mail is required.'),
        ('password', 'The password is required.'),
        ('password2', 'The confirmation password is required.')
    ])
    def test_fields_are_not_empty(self, field, error_message):
        # Changing the current field's value to an
        # empty string
        self.form_data[field] = ''

        # Getting the url to the view
        url = reverse('authors:register_create')

        # Getting the response to submit the form
        # Because the register_create page redirects the user
        # to other page, the follow=True attribute is required.
        response = self.client.post(url, data=self.form_data, follow=True)

        # Assertions:
        # Check if the error message is in the errors list
        self.assertIn(
            error_message,
            response.context['form'].errors.get(field),
            msg=f"Empty {field} error message wasn't found in the error list"
        )
        # Check if the error message is displayed in the html
        self.assertIn(
            error_message,
            response.content.decode('utf-8'),
            msg=f"The empty {field} error message wasn't found in the HTML")

    # TEST to check if the min_length to the username is being respected
    def test_username_min_length_is_4(self):

        # Changing the username value to 3 characters
        self.form_data['username'] = '123'

        # Getting the url to the view
        url = reverse('authors:register_create')

        # Sending the form with the invalid username
        # The follow attribute is required because this view uses redirect()
        response = self.client.post(url, data=self.form_data, follow=True)

        # Error message expected
        message = ('Username requires a minimum of 4 characters.')

        # Assertioons:
        # Check if the error message is in the error list
        self.assertIn(
            message,
            response.context['form'].errors.get('username'),
            msg='MIN_LEGNTH: Invalid username (less than 4 chars) '
            'error was not found in the error list.',)

        # Check if the error message is displayed in the HTML
        self.assertIn(
            message,
            response.content.decode('utf-8'),
            msg='MIN_LENGTH: Invalid username (less than 4 chars) error '
            'was not displayed in the HTML.',)

        # Altering the username to a valid one, with 4 characters
        self.form_data['username'] = '1234'

        # Getting the new response
        response = self.client.post(url, data=self.form_data, follow=True)

        # New assertion:
        # Check if the error message is NOT displayed in the HTML
        self.assertNotIn(
            message,
            response.content.decode('utf-8'),
            msg='MIN_LENGTH: Valid username (4 chars or more) was '
            'considered invalid.',)

    # TEST if the username's max length is being respected.
    def test_username_max_length_is_150(self):

        # Changing the username to an invalid one with 151 characters
        self.form_data['username'] = 'a'*151

        # Getting the url to the view
        url = reverse('authors:register_create')

        # Getting the response after sending the form with the invalid username
        # The follow attribute is required because this view uses redirect()
        response = self.client.post(url, data=self.form_data, follow=True)

        # Error message expected
        message = ('Username requires a maximum of 150 characters.')

        # Assertions:
        # Check if the error message is in the error list
        self.assertIn(
            message,
            response.context['form'].errors.get('username'),
            msg="MAX_LENGHT: Invalid username (more than 150 chars) "
            "error was not found in the error list.",)

        # Check if the error message is displayed in the HTML

        self.assertIn(message, response.content.decode(
            'utf-8'),
            msg="MAX_LENGHT: Invalid username (more than 150 chars) "
            "error was not displayed in the HTML.",)

        # Changing the username to a valid one with 150 characters
        self.form_data['username'] = 'a'*150

        # Getting the new response by sending the form
        response = self.client.post(url, data=self.form_data, follow=True)

        # Assertions:
        # Check if the error message is NOT displayed in the HTML
        self.assertNotIn(message, response.content.decode(
            'utf-8'),
            msg='MAX_LENGTH: Valid username (150 chars or less) was considered'
            ' invalid.')

    # TEST to check if the password requirements are being respected.
    def test_password_has_uppercase_lowercase_and_numbers(self):
        # UPPERCASE CHECK
        # Changing the password to an invalid one without uppercase letters
        self.form_data['password'] = 'ascd1234'

        # Getting the url to the view
        url = reverse('authors:register_create')

        # Getting the response after sending the form to with invalid password
        # The follow attribute is required because this view uses redirect()
        response = self.client.post(url, self.form_data, follow=True)

        # Error message expected
        error_message = (
            'Remember: The password must have at least one uppercase letter, '
            'one lowercase and one number. The length should be at least '
            '8 characters.')

        # Assertions:
        # Check if the error message is in the error list
        self.assertIn(
            error_message,
            response.context['form'].errors.get('password'),
            msg="PASSWORD REQUIREMENTS: Uppercase absence was not considered "
            "an error (error not found in the error list).",)

        # Check if the error message is displayed in the HTML
        self.assertIn(
            error_message,
            response.content.decode('utf-8'),
            msg="PASSWORD REQUIREMENTS: Uppercase absence was not considered "
            "an error (error not displayed in the HTML).",)

        # LOWERCASE CHECK
        # Changing the password to an invalid one without lowercase letters
        self.form_data['password'] = 'ASCD1234'

        # Getting the response after sending the form to with invalid password
        # The follow attribute is required because this view uses redirect()
        response = self.client.post(url, self.form_data, follow=True)

        # Assertions:
        # Check if the error message is in the error list
        self.assertIn(
            error_message,
            response.context['form'].errors.get('password'),
            msg="PASSWORD REQUIREMENTS: Lowercase absence was not considered "
            "an error (error not found in the error list).",)

        # Check if the error message is displayed in the HTML
        self.assertIn(
            error_message,
            response.content.decode('utf-8'),
            msg="PASSWORD REQUIREMENTS: Lowercase absence was not considered "
            "an error (error not displayed in the HTML).",)

        # NUMBERS CHECK
        # Changing the password to an invalid one without lowercase letters
        self.form_data['password'] = 'ASCDascd'

        # Getting the response after sending the form to with invalid password
        # The follow attribute is required because this view uses redirect()
        response = self.client.post(url, self.form_data, follow=True)

        # Assertions:
        # Check if the error message is in the error list
        self.assertIn(
            error_message,
            response.context['form'].errors.get('password'),
            msg="PASSWORD REQUIREMENTS: Numbers absence was not considered "
            "an error (error not found in the error list).",)

        # Check if the error message is displayed in the HTML
        self.assertIn(
            error_message,
            response.content.decode('utf-8'),
            msg="PASSWORD REQUIREMENTS: Numbers absence was not considered "
            "an error (error not displayed in the HTML).",)

        # VALID PASSWORD
        # Changing the password to a valid one
        self.form_data['password'] = 'AAAaaa11'

        # Getting the new response
        response = self.client.post(url, self.form_data, follow=True)

        # Assertions:
        # Check if the error message is NOT displayed in the HTML
        self.assertNotIn(
            error_message,
            response.content.decode('utf-8'),
            msg="PASSWORD REQUIREMENTS: Valid password was considered an error"
            " (error message displayed in the HTML).",)

    # TEST to check if the confirmation password and password are equal
    def test_password_and_confirmation_validation(self):

        # Getting the url to the view
        url = reverse('authors:register_create')

        # Getting the response after sending valid passwords
        # The follow attribute is required because this view uses redirect()

        response = self.client.post(url, data=self.form_data, follow=True)

        # Error message expected if the passwords are differents
        error_message = ("The passwords must be equal.")

        # Assertion:
        # Check if the error message is NOT displayed in the HTML
        self.assertNotIn(
            error_message, response.content.decode('utf-8'),
            msg="PASSWORD CONFIRMATION: Unmatching password error message "
            " found in the HTML when it shouldn't be found.")

        # Changing the passowrd to another valid one, but keeping it different
        # from the confirmation one
        self.form_data['password'] = 'Str0ngPassword2'

        # Getting the new response after sending the form
        response = self.client.post(url, data=self.form_data, follow=True)

        # Assertions:
        # Check if the error message is in the error list
        self.assertIn(
            error_message,
            response.context['form'].errors.get('password2'),
            msg="PASSWORD CONFIRMATION: Unmatching password error message "
            "not found in the error list.",)

        # Check if the error message is displayed in the HTML
        self.assertIn(
            error_message, response.content.decode('utf-8'),
            msg="PASSWORD CONFIRMATION: Unmatching password error message "
            "not displayed in the HTML.",)

    # TEST to check if the e-mail is unique
    def test_register_email_must_be_unique(self):

        # Getting the url to the view
        url = reverse('authors:register_create')

        # Sending the form to register the setUp user
        # The follow attribute is required because this view uses redirect()
        self.client.post(url, data=self.form_data, follow=True)

        # Getting the response after sending the same user data
        response = self.client.post(url, data=self.form_data, follow=True)

        # Expected error message
        error_message = ('This e-mail is already in use.')

        # Assertions:
        # Check if the error message is in the error list
        self.assertIn(
            error_message,
            response.context['form'].errors.get('email'),
            msg="UNIQUE E-MAIL: The unique e-mail error wasn't found"
            "in the error list  although it was expected to.",)

        # Check if the error message is displayed in the HTML
        self.assertIn(
            error_message,
            response.content.decode('utf-8'),
            msg="UNIQUE E-MAIL: The unique e-mail error wasn't displayed"
                "in the HTML, although it was expected to.",)

    # TEST if the author can log in
    def test_author_created_can_log_in(self):

        # Getting the url to the view
        url = reverse('authors:register_create')

        # Changing the user data and password
        # just to be easy to check the data here
        self.form_data.update({
            'username': 'my_user',
            'password': '1234ABcd',
            'password2': '1234ABcd'
        })

        # Register the user
        self.client.post(url, data=self.form_data)

        # Check if the data updated above returns True when login is called.
        is_authenticated = self.client.login(
            username='my_user', password='1234ABcd')

        # Assertion
        # Checking if the login returned True
        self.assertTrue(
            is_authenticated,
            msg="Valid user was not allowed to login. "
            "(login function returned false)",)
