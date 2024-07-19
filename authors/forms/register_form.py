from django import forms  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from utils.django_forms import add_placeholder, strong_password  # type: ignore
from django.utils.translation import gettext_lazy as _


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['first_name'], _('Your first name'))
        add_placeholder(self.fields['last_name'], _('Your last name'))
        add_placeholder(self.fields['email'], _('Your e-mail'))
        add_placeholder(self.fields['username'], _('Your username'))
        add_placeholder(self.fields['password'], _('Your password'))
        add_placeholder(self.fields['password2'], _('Repeat your password'))

    first_name = forms.CharField(
        error_messages={
            'required': _('The first name must not be empty.')
        },
        required=True,
        label=_('First Name'),
    )

    last_name = forms.CharField(
        error_messages={
            'required': _('The last name must not be empty.')
        },
        required=True,
        label=_('Last Name'),
    )

    username = forms.CharField(
        required=True,
        label=_('Username'),
        help_text=_(
            'Required. Length between 4 and 150 characters. Accepts uppercase'
            ' and lowercase letters, numbers, and special characters.'),
        error_messages={
            'required': _('The username is required.'),
            'min_length': _('Username requires a minimum of 4 characters.'),
            'max_length': _('Username requires a maximum of 150 characters.'),
            'unique': _('This username is not available.')

        },
        min_length=4,
        max_length=150
    )

    email = forms.EmailField(
        error_messages={
            'required': _('The e-mail is required.'),
            'invalid': _('The e-mail must be a valid one.'),
        },
        required=True,
        label=_('E-mail'),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': _('The password is required.')
        },
        help_text=_(
            'Password must have at least one uppercase letter, '
            'one lowercase and one number. The length should be at least '
            '8 characters.'),
        validators=[strong_password],

        label=_('Password')
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        label=_('Repeat your password'),
        error_messages={
            'required': _('The confirmation password is required.')
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
                _('This e-mail is already in use.'), code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:

            password_confirmation_error = forms.ValidationError(
                _("The passwords must be equal."),
                code='invalid'
            )

            raise forms.ValidationError(
                {

                    'password2': [password_confirmation_error]
                }
            )
