from django.contrib.messages import constants  # type: ignore

MESSAGE_TAGS = {
    constants.DEBUG: 'message-debug',
    constants.ERROR: 'message-error',
    constants.SUCCESS: 'message-success',
    constants.WARNING: 'message-warning',
    constants.INFO: 'message-info',

}
