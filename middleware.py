from . import log
from . import settings
from .log_object import LogObject


class DjangoLoggingMiddleware:
    @staticmethod
    def process_exception(request, exception):
        log.error(LogObject(request, exception))

    @staticmethod
    def process_response(request, response):
        if request.path_info.startswith(tuple(settings.IGNORED_PATHS)):
            return response

        log.info(LogObject(request, response))
        return response
