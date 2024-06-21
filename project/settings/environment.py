import os
from pathlib import Path
from utils.environment import get_env_variables, parse_comma_sep_to_list


if os.environ.get('DEBUG', None) is None:
    from dotenv import load_dotenv
    load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG') == '1' else False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WSGI_APPLICATION = 'project.wsgi.application'


ROOT_URLCONF = 'project.urls'


ALLOWED_HOSTS = parse_comma_sep_to_list(
    get_env_variables('ALLOWED_HOSTS'))  # type: ignore

CSFR_TRUSTED_ORIGINS = parse_comma_sep_to_list(
    get_env_variables('CSFR_TRUSTED_ORIGINS'))
