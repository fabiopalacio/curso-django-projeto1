
from django.forms import ValidationError  # type:ignore
from .test_recipe_base import RecipeTestBase


class RecipesCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()

    def test_category_model_str_representation(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_category_model_max_length_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
