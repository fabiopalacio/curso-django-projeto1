import time
from django.test import LiveServerTestCase  # type: ignore
import pytest  # type: ignore

from utils.browser import make_firefox_browser  # type: ignore


@pytest.mark.functionaltest
class AuthorsBaseTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = make_firefox_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, qty=5):
        time.sleep(qty)

    def test_the_test(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        self.sleep()
