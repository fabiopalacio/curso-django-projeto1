from django.urls import reverse  # type: ignore

from authors.forms import RegisterForm


from unittest import TestCase
from django.test import TestCase as DjangoTestCase  # type: ignore
from parameterized import parameterized  # type: ignore


class AuthorsRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('first_name', 'Your first name'),
        ('last_name', 'Your last name'),
        ('email', 'Your e-mail'),
        ('username', 'Your username'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password')
    ])
    def test_field_placeholder_is_correct(self, field, exp_placeholder):
        form = RegisterForm()
        placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(
            placeholder, exp_placeholder,
            msg=f"The {field}'s placeholder is incorrect")

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
        form = RegisterForm()
        help_text = form[field].field.help_text
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


class AuthorsRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'User',
            'first_name': 'John',
            'last_name': 'Silva',
            'email': 'john@mail.com',
            'password':  'Str0ngPassword',
            'password2': 'Str0ngPassword'
        }

        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'The username is required.'),
        ('first_name', 'The first name must not be empty.'),
        ('last_name', 'The last name must not be empty.'),
        ('email', 'The e-mail is required.'),
        ('password', 'The password is required.'),
        ('password2', 'The confirmation password is required.')
    ])
    def test_fields_are_not_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get(field))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_min_length_is_4(self):
        self.form_data['username'] = '123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        message = ('Username requires a minimum of 4 characters.')

        self.assertIn(
            message,
            response.context['form'].errors.get('username'),
            msg='The error message was not found in the response error list.')
        self.assertIn(
            message,
            response.content.decode('utf-8'),
            msg='The error message was not found in the response html.')

        self.form_data['username'] = '1234'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(
            message,
            response.content.decode('utf-8'),
            msg='The error message was not found in the response html.')

    def test_username_max_length_is_150(self):
        self.form_data['username'] = 'a'*151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        message = ('Username requires a maximum of 150 characters.')

        self.assertIn(
            message,
            response.context['form'].errors.get('username'),
            msg='The error message was not found in the response error list.')

        self.assertIn(message, response.content.decode(
            'utf-8'),
            msg='The error message was not found in the response html.')

        self.form_data['username'] = 'a'*150
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(message, response.content.decode(
            'utf-8'),
            msg='The error message was not found in the response html.')

    def test_password_has_uppercase_lowercase_and_numbers(self):
        self.form_data['password'] = 'asc123'
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)
        error_message = (
            'Remember: The password must have at least one uppercase letter, '
            'one lowercase and one number. The length should be at least '
            '8 characters.')
        self.assertIn(
            error_message, response.context['form'].errors.get('password'))
        self.assertIn(error_message, response.content.decode('utf-8'))

        self.form_data['password'] = 'AAaa12@@'
        response = self.client.post(url, self.form_data, follow=True)

        self.assertNotIn(error_message, response.content.decode('utf-8'))

    def test_password_and_confirmation_validation(self):

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        error_message = ("The passwords must be equal.")

        self.assertNotIn(
            error_message, response.content.decode('utf-8'),
            msg="Unmatching password error message found in the"
            " html when it shouldn't be found.")

        self.form_data['password'] = 'Str0ngPassword2'
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(
            error_message, response.content.decode('utf-8'),
            msg='Unmatching password error message not found in the html.')

        self.assertIn(
            error_message, response.context['form'].errors.get('password2'),
            msg='Unmatching password error message not'
            ' found in the error list')

    def test_register_email_must_be_unique(self):

        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)

        error_message = ('This e-mail is already in use.')
        self.assertIn(
            error_message,
            response.context['form'].errors.get('email'),
            msg=" The unique e-mail error wasn't found in the error list.")
