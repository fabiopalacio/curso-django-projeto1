import dotenv
import django


def pytest_sessionstart(session):
    dotenv.load_dotenv()
    django.setup()
