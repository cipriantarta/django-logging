import logging
import logging.config
import os

import sys

from . import settings

LOG_LEVEL = settings.LOG_LEVEL.upper()
LOG_HANDLERS = ['default']

if settings.CONSOLE_LOG:
    LOG_HANDLERS.append('console')
if settings.DEBUG:
    LOG_HANDLERS.append('debug')
if settings.SQL_LOG:
    LOG_HANDLERS.append('sql')

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
        'sql': {
            'format': '[%(levelname)s - %(created)s] %(duration)s %(sql)s %(params)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'django_logging.handlers.ConsoleHandler',
            'formatter': 'verbose',
            'stream': sys.stderr
        },
        'default': {
            'level': 'INFO',
            'class': 'django_logging.handlers.AppFileHandler',
            'formatter': 'verbose',
            'maxBytes': settings.ROTATE_MB * 1024 * 1024,
            'backupCount': settings.ROTATE_COUNT,
            'filename': '{}/app.log'.format(settings.LOG_PATH)
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'django_logging.handlers.DebugFileHandler',
            'formatter': 'verbose',
            'maxBytes': settings.ROTATE_MB * 1024 * 1024,
            'backupCount': settings.ROTATE_COUNT,
            'filename': '{}/debug.log'.format(settings.LOG_PATH)
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'django_logging.handlers.SQLFileHandler',
            'formatter': 'sql',
            'maxBytes': settings.ROTATE_MB * 1024 * 1024,
            'backupCount': settings.ROTATE_COUNT,
            'filename': '{}/sql.log'.format(settings.LOG_PATH)
        }
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
    logger.setLevel(LOG_LEVEL)
    return logger
