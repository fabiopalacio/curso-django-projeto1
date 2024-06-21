
from .middlewares import MIDDLEWARE
from .installed_apps import INSTALLED_APPS

# DJANGO DEBUG TOOLBAR
INTERNAL_IPS = [
    '127.0.0.1',
]


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    *MIDDLEWARE,
]

INSTALLED_APPS = [
    *INSTALLED_APPS,
    'debug_toolbar',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: False,  # disables it
    # '...
}
