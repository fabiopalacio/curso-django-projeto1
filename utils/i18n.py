from django.utils import translation


def set_language():
    return translation.get_language()
