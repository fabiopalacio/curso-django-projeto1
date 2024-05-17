import re
from django import forms  # type: ignore

from django.contrib.auth.models import User  # type: ignore


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_value):
    add_attr(field, 'placeholder', placeholder_value)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise forms.ValidationError((
            'Remember: The password must have at least one uppercase letter, '
            'one lowercase and one number. The length should be at least '
            '8 characters.'), code='invalid'
        )


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['first_name'], 'Your first name')
        add_placeholder(self.fields['last_name'], 'Your last name')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['password'], 'Your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    first_name = forms.CharField(
        error_messages={
            'required': 'The first name must not be empty.'
        },
        required=True,
        label='First Name',
    )

    last_name = forms.CharField(
        error_messages={
            'required': 'The last name must not be empty.'
        },
        required=True,
        label='Last Name',
    )

    username = forms.CharField(
        required=True,
        label='Username',
        help_text='Required. Length between 4 and 150 characters. Accepts '
        'uppercase and lowercase letters, numbers, and special characters.',
        error_messages={
            'required': 'The username is required.',
            'min_length': 'Username requires a minimum of 4 characters.',
            'max_length': 'Username requires a maximum of 150 characters.',
            'unique': 'This username is not available.'

        },
        min_length=4,
        max_length=150
    )

    email = forms.EmailField(
        error_messages={
            'required': 'The e-mail is required.',
            'invalid': 'The e-mail must be a valid one.',
        },
        required=True,
        label='E-mail',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': 'The password is required.'
        },
        help_text='Password must have at least one uppercase letter, '
        'one lowercase and one number. The length should be at least '
        '8 characters.',
        validators=[strong_password],

        label='Password'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        label='Repeat your password',
        error_messages={
            'required': 'The confirmation password is required.'
        },

    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise forms.ValidationError(
                'This e-mail is already in use.', code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:

            password_confirmation_error = forms.ValidationError(
                "The passwords must be equal.",
                code='invalid'
            )

            raise forms.ValidationError(
                {

                    'password2': [password_confirmation_error]
                }
            )
