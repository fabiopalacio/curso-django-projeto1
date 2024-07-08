
from tag.models import Tag
from django.test import TestCase  # type: ignore
from django.contrib.auth.models import User  # type: ignore

from recipes.models import Category, Recipe

# RECIPE MIXIN class:
# Holds the basic methods to work with the recipes during tests.


class RecipeMixin:

    # METHOD to create a new category
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    # METHOD to create a new author
    def make_author(
        self,
        first_name='Joe',
        last_name='Smith',
        email='joe_smith@server.com',
        password='123456',
        username='joeSmith'
    ):
        return User.objects.create_user(first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        password=password,
                                        username=username)

    # METHOD to create a new recipe
    def make_recipe(
            self,
            category_data=None,
            author_data=None,
            title='My Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
            cover='',):

        # Check if category_data is empty.
        # If so, it calls the make_category method

        if category_data is None:
            category_data = self.make_category(name='Default Category')

        # Check if author_data is empty.
        # If so, creates a empty dictionary to be passed to
        # the make_author() method
        if author_data is None:
            author_data = {}

        return Recipe.objects.create(  # noqa: F841
            category=category_data,
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            cover=cover)

    # METHOD to create a group of recipes.
    # The category_data is required to avoid creating
    # individuals categories to each recipe when
    # it is required them to be in the same one
    def make_recipes_in_batch(self, qty=7, category_data=None):
        recipes = []
        for i in range(qty):
            recipe = self.make_recipe(
                slug=f'recipe-{i}', title=f'This is recipe {i}',
                author_data={'username': f'{i}'},
                category_data=category_data
            )
            recipes.append(recipe)
        return recipes

    def make_tag(self, tag_name='GenericTag'):
        return Tag.objects.create(name=tag_name)

    # CLASS to be used in the recipes app tests.
    # It extends the TestCase and RecipeMixin classes.


class RecipeTestBase(TestCase, RecipeMixin):
    # SETUP
    def setUp(self) -> None:
        return super().setUp()
