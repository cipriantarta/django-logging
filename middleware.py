from . import log


class GBLoggingMiddleware:
    def process_response(self, request, response):
        log.info(request)
        return response
