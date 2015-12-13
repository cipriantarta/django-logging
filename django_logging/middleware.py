from django.db import connection
from . import log
from . import settings
from .log_object import LogObject, ErrorLogObject, SqlLogObject


class DjangoLoggingMiddleware(object):
    @staticmethod
    def process_exception(request, exception):
        error = ErrorLogObject(request, exception)
        log.error(error)
        return error.response

    @staticmethod
    def process_response(request, response):
        for query in connection.queries:
            log.debug(SqlLogObject(query))
        if request.path_info.startswith(tuple(settings.IGNORED_PATHS)):
            return response

        if response.status_code == 500:
            return response
        elif 400 <= response.status_code < 500:
            log.warning(LogObject(request, response))
        else:
            log.info(LogObject(request, response))
        return response
