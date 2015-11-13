Django Logging
==============

A Django library that logs request, response and exception details in a JSON document.
It users the python rotation mechanism to rotate the file logs, but the rotation files will be gziped.

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