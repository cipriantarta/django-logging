import sys
from django.conf import settings as django_settings


class GBLoggingSettings:
    __settings = None

    def __init__(self):
        user_settings = getattr(django_settings, 'GB_LOGGING', None)
        self.__settings = dict(
            DEBUG=django_settings.DEBUG,
            CONSOLE_LOG=True,
            LOG_LEVEL='debug',
            INFO=False,
            DISABLE_EXISTING_LOGGERS=True,
            LOG_PATH='{}/logs'.format(django_settings.BASE_DIR),
            IGNORED_PATHS=['/admin', '/static', '/favicon.ico'],
            RESPONSE_FIELDS=('status', 'reason', 'charset', 'headers', 'content'),
            CONTENT_JSON_ONLY=True,
            ROTATE_MB=100*1024*1024,
            ROTATE_COUNT=10
        )

        try:
            self.__settings.update(user_settings)
        except TypeError:
            pass

    def __getattr__(self, name):
        return self.__settings.get(name)
            

sys.modules[__name__] = GBLoggingSettings()
