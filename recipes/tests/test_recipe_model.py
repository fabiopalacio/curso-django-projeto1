from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError  # type: ignore
from parameterized import parameterized  # type: ignore


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_with_no_boolean_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='MyNewCategory'),
            author=self.make_author(username='NewUsername'),
            title='My Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65)
    ])
    def test_recipe_fiels_max_len(self, field, max_length):

        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_default(self):
        recipe = self.make_recipe_with_no_boolean_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html is not False by default.')

    def test_recipe_is_published_is_false_default(self):
        recipe = self.make_recipe_with_no_boolean_defaults()
        self.assertFalse(recipe.is_published,
                         msg='Recipe is_published is not False by default')
