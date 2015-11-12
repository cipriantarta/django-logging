import logging
import os
from . import settings

LOG_LEVEL = settings.LOG_LEVEL.upper()
LOG_HANDLERS = ['default']

if settings.CONSOLE_LOG:
    LOG_HANDLERS.append('console')

if not os.path.exists(settings.LOG_PATH):
    try:
        os.makedirs(settings.LOG_PATH)
    except Exception as e:
        raise Exception('Unable to configure logger. Can\'t create LOG_PATH: {}'.format(settings.LOG_PATH))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': settings.DISABLE_EXISTING_LOGGERS,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s - %(created)s], file:%(module)s.py, func:%(funcName)s, ln:%(lineno)s: %(message)s'
        },
        'simple': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'django-logging.handlers.ConsoleHandler',
            'formatter': 'verbose',
        },
        'default': {
            'level': settings.LEVEL,
            'class': 'django-logging.handlers.AppFileHandler',
            'formatter': 'verbose',
            'maxBytes': settings.ROTATE_MB,
            'backupCount': settings.ROTATE_COUNT,
            'filename': '{}/app.log'.format(settings.LOG_PATH)
        },
    },
    'loggers': {
        'dl_logger': {
            'handlers': LOG_HANDLERS,
            'level': LOG_LEVEL,
            'propagate': True
        },
    }
}
logging.config.dictConfig(LOGGING)


def get_logger():
    logger = logging.getLogger('dl_logger')
    logger.setLevel(logging.getLevelName(LOG_LEVEL))
    return logger
