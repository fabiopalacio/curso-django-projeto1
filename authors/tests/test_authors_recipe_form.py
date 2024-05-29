from authors.forms.recipe_form import AuthorsRecipeForm
from django.test import TestCase

# CLASS to run unit and integration tests to
# the Recipe Form


class AuthorsRecipeFormTest(TestCase):

    # TEST if invalid fields append errors in the
    # ._my_errors dictionary
    def test_invalid_fields_clean_field_errors(self):

        # Creating a form with invalid data
        # The invalid data inserted here are the
        # ones being checked in clean methods.
        # They are:
        #   title: must have more than 5 chars and different from description
        #   description: must be different from the title
        #   preparation_time: must be positive number
        #   servings: must be positive number

        form = AuthorsRecipeForm(data={
            'title': 'Teste',
            'description': 'Teste',
            'preparation_time': -12,
            'preparation_time_unit': 'Horas',
            'servings': -1,
            'servings_unit': 'Pessoas',

            'preparation_steps': 'Some steps',
        })

        # is_valid() method calls the clean methods.
        # If an error is found, its message is inserted in the
        # ._my_errors dictionary
        form.is_valid()

        # ASSERTIONS:
        # Check if the length title error is in ._my_errors
        self.assertIn(
            'Must have at least 6 characters.',
            form._my_errors['title'],
            msg='RECIPE FORM - CLEAN_FIELD: Title with less than 6 chars was '
            'accepted when it WAS NOT expected to. '
            f'Title inserted: {form["title"].data}')

        # Check if the title must be different from description error
        # is in ._my_errors
        self.assertIn(
            'Must be different from description.',
            form._my_errors['title'],
            msg='RECIPE FORM - CLEAN_FIELD: Title must be different from '
            'description error not found. '
            f'Title inserted: {form["title"].data}'
            f'Description inserted: {form["description"].data}'
        )

        # Check if the description must be different from title error
        # is in ._my_errors
        self.assertIn(
            'Must be different from title.',
            form._my_errors['description'],
            msg='RECIPE FORM - CLEAN_FIELD: Description must be different from'
            ' title error not found. '
            f'Title inserted: {form["title"].data}'
            f'Description inserted: {form["description"].data}'
        )

        # Check if preparation_time must be positive error is in ._my_errors
        self.assertIn(
            'Must be a positive number.',
            form._my_errors['preparation_time'],
            msg='RECIPE FORM - CLEAN_FIELD: NEGATIVE preparation time WAS NOT '
            'rejected. '
            f'Preparation time inserted: {form["preparation_time"].data}')

        # Check if servings must be positive error is in ._my_errors
        self.assertIn(
            'Must be a positive number.',
            form._my_errors['servings'],
            msg='RECIPE FORM - CLEAN_FIELD: NEGATIVE servings WAS NOT '
            'rejected. '
            f'Servings inserted: {form["servings"].data}')

    # TEST to check if valid fields do not add errors to .my_errors
    def test_valid_fields_clean_field_without_errors(self):
        # Creating a valid form
        form = AuthorsRecipeForm(data={
            'title': 'A valid title',
            'description': 'A valid description',
            'preparation_time': 12,
            'preparation_time_unit': 'Horas',
            'servings': 1,
            'servings_unit': 'Pessoas',
            'preparation_steps': 'Some steps',
        })

        # Calling is_valid(), which calls clean() methods
        form.is_valid()

        # ASSERTIONS:
        # Check if form._my_errors is empty
        self.assertFalse(
            form._my_errors,
            msg="RECIPE FORM - CLEAN DATA: Form raised erros when "
            "it should not.")

        # Creating an invalid form to make the inverse test
        form = AuthorsRecipeForm({
            'title': 'A valid text',
            'description': 'A valid text',
            'preparation_time': 12,
            'preparation_time_unit': 'Horas',
            'servings': 1,
            'servings_unit': 'Pessoas',
            'preparation_steps': 'Some steps',
        })
        # Calling the clean() methods
        form.is_valid()

        # Check if form._my_errors is not empty
        self.assertTrue(
            form._my_errors,
            msg="RECIPE FORM - CLEAN DATA: Form did not raise erros when "
            "it should.")
