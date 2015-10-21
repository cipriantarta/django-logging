import logging
import os
import sys
from . import settings

LOG_LEVEL = settings.LOG_LEVEL.upper()
LOG_HANDLERS = ['error']

if settings.CONSOLE_LOG:
    LOG_HANDLERS.append('console')

if settings.INFO_LOG:
    LOG_HANDLERS.append('info')

if settings.DEBUG_LOG:
    LOG_HANDLERS.append('debug')

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
        'debug': {
            'level': 'DEBUG',
            'class': 'django-logging.handlers.DebugFileHandler',
            'formatter': 'verbose',
            'filename': '{}/debug.log'.format(settings.LOG_PATH)
        },
        'info': {
            'level': 'INFO',
            'class': 'django-logging.handlers.InfoFileHandler',
            'formatter': 'verbose',
            'filename': '{}/info.log'.format(settings.LOG_PATH)
        },
        'error': {
            'level': 'ERROR',
            'class': 'django-logging.handlers.ErrorFileHandler',
            'formatter': 'verbose',
            'filename': '{}/error.log'.format(settings.LOG_PATH)
        },
    },
    'loggers': {
        'gb_logger': {
            'handlers': LOG_HANDLERS,
            'level': LOG_LEVEL,
            'propagate': True
        },
    }
}
logging.config.dictConfig(LOGGING)


def get_logger():
    logger = logging.getLogger('gb_logger')
    logger.setLevel(logging.getLevelName(LOG_LEVEL))
    return logger
