from django.test import TestCase  # type: ignore
from django.urls import reverse  # type: ignore
# Create your tests here.


class RecipeURLsTest(TestCase):

    def test_recipe_home_url_is_correct(self):
        home_url = reverse('recipes:home')
        # Checking if the recipes:home url is '/'
        self.assertEqual(home_url, '/')
