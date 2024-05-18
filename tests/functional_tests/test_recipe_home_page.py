import time
from django.test import LiveServerTestCase
# In case you need static files, use the following Live server:
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_firefox_browser
from selenium.webdriver.common.by import By


class RecipeHomePageFunctionalTest(LiveServerTestCase):
    def sleep(self, seconds=5):
        time.sleep(seconds)

    def test_the_test(self):
        browser = make_firefox_browser()
        browser.get(self.live_server_url)
        self.sleep(1)

        body = browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('No recipes found here...', body.text)

        browser.quit()
