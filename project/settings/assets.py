
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

from project.settings.environment import BASE_DIR


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'base_static'
]
STATIC_ROOT = BASE_DIR / 'static'
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'
