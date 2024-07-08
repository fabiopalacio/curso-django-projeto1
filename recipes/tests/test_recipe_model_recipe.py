from django.core.exceptions import ValidationError  # type: ignore
from parameterized import parameterized  # type: ignore

from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase

# CLASS to test MODEL RECIPE


class RecipesRecipeModelTest(RecipeTestBase):
    # SETUP: run before each test
    def setUp(self) -> None:
        # Create a generic recipe
        self.recipe = self.make_recipe()
        return super().setUp()

    # METHOD to create a recipe without passing boolean attributes.
    # They have False as default value
    def make_recipe_with_no_boolean_defaults(self):
        # Fill a Recipe object with the others attributes
        recipe = Recipe(
            category=self.make_category(name='MyNewCategory'),
            author=self.make_author(username='NewUsername'),
            title='A new Recipe',
            description='Recipe Description',
            slug='recipe-slug-for-no-defaults',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )
        # Check if there are any errors in the objects
        recipe.full_clean()

        # Save the recipe to the test database
        recipe.save()

        # Return the created recipe
        return recipe

    # TEST if the field's max length is being respected
    # Using parameterized to run subtests
    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65)
    ])
    def test_recipe_fields_max_len(self, field, max_length):
        # Set the field to 1 more character than allowed by the model
        setattr(self.recipe, field, 'A' * (max_length + 1))

        # Check if the full_clean() raises a validation error
        # It should raises a ValidationError, with which the test passes.
        # If it doesn't, the test fails and send a message
        try:
            self.recipe.full_clean()
        except ValidationError:
            ...
        else:
            self.fail(
                "RECIPE MODEL - MAX-LENGTH: A validation error was expected "
                "but not found.",)

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    # TEST if preparation_steps_is_html generated is False
    def test_recipe_preparation_steps_is_html_is_false_default(self):

        # Create a recipe without the boolean defaults
        recipe = self.make_recipe_with_no_boolean_defaults()

        # Check if the value generate by default is False
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='RECIPE MODEL - PREPARATION STEPS IS HTML: '
            'Recipe preparation_steps_is_html attribute is not '
            'False by default.',)

    # TEST if is_published attribute is false by default
    def test_recipe_is_published_is_false_default(self):
        # Create a recipe without the boolean defaults
        recipe = self.make_recipe_with_no_boolean_defaults()

        # Check if the recipe.is_published is false generated is False
        self.assertFalse(
            recipe.is_published,
            msg='RECIPE MODEL - IS_PUBLISHED: '
            'Recipe is_published attribute is not False by default.',)

    # TEST if the Recipe string representation returns the Recipe's name
    def test_recipe_string_representation(self):
        # Saving the new recipe title
        needed = 'Testing Recipe String'

        # Passing the new title to the recipe
        self.recipe.title = needed

        # Cleaning and saving the updated recipe
        self.recipe.full_clean()
        self.recipe.save()

        # Checking if the self.recipe returns the recipe title
        self.assertEqual(
            str(self.recipe), needed,
            msg=f'Expect: "{needed}" but found: "{str(self.recipe)}"')

    def test_recipe_slugify_is_working(self):
        recipe = Recipe(
            category=self.make_category(name='MyNewCategory'),
            author=self.make_author(username='NewUsername'),
            title='A long title recipe to test slug',
            description='Recipe Description',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )

        expected_slug = 'a-long-title-recipe-to-test-slug'
        recipe.save()
        self.assertEqual(
            recipe.slug,
            expected_slug,
            msg="RECIPE MODEL - SLUGIFY: Slug created was not what the test "
            f"expected. Expected: {expected_slug}. "
            f"Found: {recipe.slug}"
        )
