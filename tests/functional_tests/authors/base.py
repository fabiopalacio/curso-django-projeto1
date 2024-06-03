from django.test import LiveServerTestCase  # type: ignore

import time

from selenium.webdriver.common.by import By


from utils.browser import make_firefox_browser


# CLASS BASE to some authors views tests
# This class create the browser in setup method,
# quit the browser in the tearDown method,
# and create two methods used by some tests:
# sleep method -> used to wait page to load
# get_by_id -> return the web_element with the passed id
class AuthorsBaseTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = make_firefox_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, qty=5):
        time.sleep(qty)

    def get_by_id(self, web_element, id):
        return web_element.find_element(By.ID, id)
