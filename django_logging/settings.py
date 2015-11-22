import sys
from django.conf import settings as django_settings


class DjangoLoggingSettings:
    __settings = None

    def __init__(self):
        user_settings = getattr(django_settings, 'DJANGO_LOGGING', None)
        self.__settings = dict(
            DEBUG=django_settings.DEBUG,
            CONSOLE_LOG=True,
            SQL_LOG=True,
            LOG_LEVEL='debug' if django_settings.DEBUG else 'info',
            INFO=False,
            DISABLE_EXISTING_LOGGERS=True,
            LOG_PATH='{}/logs'.format(django_settings.BASE_DIR),
            IGNORED_PATHS=['/admin', '/static', '/favicon.ico'],
            RESPONSE_FIELDS=('status', 'reason', 'charset', 'headers', 'content'),
            CONTENT_JSON_ONLY=True,
            ROTATE_MB=100,
            ROTATE_COUNT=10
        )

        try:
            self.__settings.update(user_settings)
        except TypeError:
            pass

    def __getattr__(self, name):
        return self.__settings.get(name)
            

sys.modules[__name__] = DjangoLoggingSettings()
