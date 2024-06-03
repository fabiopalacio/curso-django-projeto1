import time

from django.test import LiveServerTestCase  # type: ignore
from django.contrib.auth.models import User
from django.urls import reverse

from selenium.webdriver.common.by import By

from recipes.models import Category, Recipe
from utils.browser import make_firefox_browser

# BASE CLASS to test the dashboard


class DashboardBaseTest(LiveServerTestCase):

    # setUp:
    #   Runs before each test.
    #   1) Create the browser
    #   2) Create an user to login
    #       which is required to access the dashboard page
    def setUp(self) -> None:

        # Creating the browser
        self.browser = make_firefox_browser()

        # Saving the password in a variable to be used if necessary.
        self.password = 'my_password'

        # Creating the user
        self.my_user = User.objects.create_user(
            username='my_user', password=self.password)

        return super().setUp()

    # tearDown:
    #   Runs after each test.
    #   Delete all users, recipes, and categories, to be sure that each test
    #       starts with an empty database.
    def tearDown(self) -> None:
        # Shutdown the browser
        self.browser.quit()

        # Delete all users
        users = User.objects.all()
        users.delete()

        # Delete all recipes
        recipes = Recipe.objects.all()
        recipes.delete()

        # Delete all categories
        categories = Category.objects.all()
        categories.delete()

        return super().tearDown()

    # Make recipe method:
    # Recipes are required to test some functionalities, like editing and
    # deleting a recipe. The method was recreated here, and not reused from
    # recipes test, because here was required control over some fields.
    # The fields required to be controled here are:
    #   1) slug: Some tests required more than one recipe, which were created
    #       before the browser to make it faster. But this avoided the slugify
    #       method too.
    #   2) author: Some tests required different authors, to check if only own
    #       recipes are displayed.
    #   3) is_published: Some tests required recipes to be published, to check
    #       if only unpublished recipes are displayed.
    #   4) title: To make it easy to differentiate the recipes being manipulate
    def make_recipe(self, slug, author, is_published=False, title='MyNewRecipe'):
        recipe = Recipe.objects.create(
            category=Category.objects.create(name='Category'),
            author=author,
            title=title,
            description='description 2',
            slug=slug,
            preparation_time=2,
            preparation_time_unit='Horas',
            servings=4,
            servings_unit='Pessoas',
            preparation_steps='preparation_steps',
            preparation_steps_is_html=False,
            is_published=is_published,)
        return recipe

    # Page loading is raising errors at the moment. Solution found was to wait
    # 1s every time a new page is requested. This function is for this purpose
    def sleep(self, qty=1):
        time.sleep(qty)

    # Dashboard views require user to be logged in. This method allows that.
    # It gets the login page, insert the user data and submit the form
    def login(self):

        # Getting the login page.
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Finding the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Finding the username and password fields
        # and inserting the user data created in setup()
        username_field = form.find_element(By.ID, 'id_username')
        username_field.send_keys(self.my_user.username)
        password_field = form.find_element(By.ID, 'id_password')
        password_field.send_keys(self.password)

        # Sending the form
        form.submit()
