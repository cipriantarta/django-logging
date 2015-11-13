Django Logging
==============

A Django library that logs request, response and exception details in a JSON document.
It users the python rotation mechanism to rotate the file logs, but the rotation files will be gziped.

Quick start
===========
1. Add "django_logging" to your INSTALLED_APPS settings like this:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_logging',
    )


2. Include the DjangoLoggingMiddleware middleware in your MIDDLEWARE_CLASSES like this:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        'django_logging.middleware.DjangoLoggingMiddleware',
        ...
    )

Settings
========
Inspired by Django Rest Framework, Django Logging settings are grouped in a single dictionary.

To overwrite Django Logging settings, add a dictionary in your project's settings file

.. code-block:: python

    DJANGO_LOGGING = {
        "CONSOLE_LOG": False
    }
Default Settings
----------------

.. code-block:: python

    CONSOLE_LOG = True
Log to console.


.. code-block:: python

    LOG_LEVEL = 'debug'
If settings.DEBUG is set to True, otherwise LOG_LEVEL is set to 'info'

.. code-block:: python

    DISABLE_EXISTING_LOGGERS = True
Set this to False if you want to combine with multiple loggers.

.. code-block:: python

    LOG_PATH = '{}/logs'.format(settings.BASE_DIR)
If the logs folder does not exist, it will be created.

.. code-block:: python

    IGNORED_PATHS = ['/admin', '/static', '/favicon.ico']
List of URL endpoints to ignore.

.. code-block:: python

    RESPONSE_FIELDS = ('status', 'reason', 'charset', 'headers', 'content')
List of response fields to log.

.. code-block:: python

    CONTENT_JSON_ONLY = True
Log response content only if its a JSON document.

.. code-block:: python

    ROTATE_MB = 100
Maximum size in MB that the log file can have before it gets rotated.

.. code-block:: python

    ROTATE_COUNT = 10
Maximum number of rotated log files.