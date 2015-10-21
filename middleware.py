from . import log
from . import settings
from .dl_object import DLObject


class DjangoLoggingMiddleware:
    @staticmethod
    def process_exception(request, exception):
        log.error(exception)

    @staticmethod
    def process_response(request, response):
        if not settings.ADMIN_LOGGING:
            if request.path_info.startswith(tuple(settings.IGNORED_PATHS)):
                return response

        log.info(DLObject(request, response))
        return response
