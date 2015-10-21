import sys
from django.conf import settings as django_settings


class GBLoggingSettings:
    __settings = None

    def __init__(self):
        user_settings = getattr(django_settings, 'GB_LOGGING', None)
        self.__settings = dict(
            CONSOLE_LOG=True,
            DEBUG_LOG=True,
            INFO_LOG=True,
            ERROR_LOG=True,
            FORMAT='default',
            ADMIN_LOGGING=False,
            LOG_LEVEL='debug',
            INFO=False,
            DISABLE_EXISTING_LOGGERS=True,
            LOG_PATH='{}/logs'.format(django_settings.BASE_DIR),
            IGNORED_PATHS=['/admin', '/static'],
            INFO_FIELDS=('datetime', 'method', 'path', 'request_type', 'request_length',
                         'response_status', 'response_reason')
        )

        try:
            self.__settings.update(user_settings)
        except TypeError:
            pass

    def __getattr__(self, name):
        return self.__settings.get(name)
            

sys.modules[__name__] = GBLoggingSettings()
