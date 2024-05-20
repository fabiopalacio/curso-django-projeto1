from django.test import LiveServerTestCase  # type: ignore

import time

from selenium.webdriver.common.by import By


from utils.browser import make_firefox_browser


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
