
from django.forms import ValidationError  # type:ignore

from .test_recipe_base import RecipeTestBase

# CLASS to test the Category MODEL


class RecipesCategoryModelTest(RecipeTestBase):
    # SETUP: run before each test
    # create a category before each test
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()

    # TEST if string representation returns the model's name
    def test_category_model_str_representation(self):
        self.assertEqual(str(self.category), self.category.name)

    # TEST if category.name has max length = 65
    def test_category_model_max_length_is_65_chars(self):
        # Creating an invalid category name
        # len > 65 chars
        self.category.name = 'A' * 66

        # Try to call full_clean().
        # If it raises expection, as expected, the test pass.
        # BUT it doesn't raise an expection, the else block
        # will be called and make the test fail.
        try:
            self.category.full_clean()
        except ValidationError:
            ...
        else:
            self.fail(
                "MODEL CATEGORY - MAX_LENGTH: Validation error was expected "
                "but not found.")

        # Testing a valid category name
        self.category.name = 'A' * 65

        # Try to call the full_clean()
        # If it raises an expection, the test fails.
        try:
            self.category.full_clean()
        except Exception:
            self.fail(
                'MAX_LENGTH: Category model raised exception when '
                'it was not expected.',)
