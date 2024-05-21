import os
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
FIREFOXDRIVER_NAME = 'geckodriver.exe'
FIREFOXDRIVER_PATH = ROOT_PATH / 'bin' / FIREFOXDRIVER_NAME


def make_firefox_browser(*options):
    firefox_options = webdriver.FirefoxOptions()

    if options is not None:
        for option in options:
            firefox_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        firefox_options.add_argument('--headless')

    firefox_service = Service(executable_path=FIREFOXDRIVER_PATH)
    browser = webdriver.Firefox(
        service=firefox_service, options=firefox_options)
    return browser
