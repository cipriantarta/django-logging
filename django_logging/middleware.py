import time
from django.utils.deprecation import MiddlewareMixin
from . import log
from . import settings
from .log_object import LogObject, ErrorLogObject


class DjangoLoggingMiddleware(MiddlewareMixin):
    start = None

    def process_exception(self, request, exception):
        duration = time.time() - self.start
        error = ErrorLogObject(request, exception, duration)
        log.error(error)

    def process_request(self, request):
        self.start = time.time()

    def process_response(self, request, response):
        duration = time.time() - self.start
        if request.path_info.startswith(tuple(settings.IGNORED_PATHS)):
            return response

        if response.status_code == 500:
            return response
        elif 400 <= response.status_code < 500:
            log.warning(LogObject(request, response, duration))
        else:
            log.info(LogObject(request, response, duration))
        return response
