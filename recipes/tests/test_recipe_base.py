
from django.test import TestCase  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from recipes.models import Category, Recipe


class RecipeMixin:

    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

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
            is_published=True,):

        if category_data is None:
            category_data = self.make_category(name='Default Category')

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
            is_published=is_published,)

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


class RecipeTestBase(TestCase, RecipeMixin):
    # SETUP
    def setUp(self) -> None:
        return super().setUp()
