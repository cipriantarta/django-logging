Django Logging
==============

A Django library that automatically logs request/response info in various formats, such as json, etc., which can later be sent to a log service such as sentry, splunk or others.

Quick start
===========


1. Add "django-logging" to your INSTALLED_APPS settings like this:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django-logging',
    )


2. Include the DjangoLoggingMiddleware middleware in your MIDDLEWARE_CLASSES like this:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        'django-logging.middleware.DjangoLoggingMiddleware',
        ...
    )