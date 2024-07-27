from collections import defaultdict
from django.core.exceptions import ValidationError
from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number
from django.utils.translation import gettext_lazy as _


class AuthorsRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servings_unit'].initial = 'people'
        self.fields['preparation_time_unit'].initial = 'hours'

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover',
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),

            'servings_unit': forms.Select(
                choices={
                    ('portions', 'Portions'),
                    ('pieces', 'Pieces'),
                    ('people', 'People'),
                    ('units', 'Units'), }

            ),
            'preparation_time_unit': forms.Select(
                choices={
                    ('minutes', 'Minutes'),
                    ('hours', 'Hours'),
                    ('days', 'Days'),
                }
            )
        }

        error_messages = {
            "title": {
                "required": _("Required.")
            },
            "description": {
                "required": _("Required.")
            },
            "preparation_time": {
                "required": _("Required.")
            },
            "servings": {
                "required": _("Required.")
            },
            "preparation_time_unit": {
                "required": _("Required.")
            },
            "servings_unit": {
                "required": _("Required.")
            },
            "preparation_steps": {
                "required": _("Required.")
            }
        }

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')

        if len(title) < 6:
            self._my_errors['title'].append(
                _('Must have at least 6 characters.'))

        return title

    def clean_preparation_time(self, *args, **kwargs):
        field_name = 'preparation_time'
        field = self.cleaned_data.get(field_name)
        if not is_positive_number(field):
            self._my_errors[field_name].append(
                _('Must be a positive number.'))
        return field

    def clean_servings(self, *args, **kwargs):
        field_name = 'servings'
        field = self.cleaned_data.get(field_name)
        if not is_positive_number(field):
            self._my_errors[field_name].append(
                _('Must be a positive number.'))
        return field

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self._my_errors['title'].append(
                _('Must be different from description.'))
            self._my_errors['description'].append(
                _('Must be different from title.'))

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
