from . import settings


class LogObject:
    def __init__(self, request, response):
        self.request = request
        self.response = response

    @property
    def to_dict(self):
        result = dict(
            request=self.format_request(),
            response=self.format_response()
        )
        return result

    def format_request(self):
        meta_keys = ['PATH_INFO', 'HTTP_X_SCHEME', 'REMOTE_ADDR',
                     'TZ', 'REMOTE_HOST', 'CONTENT_TYPE', 'CONTENT_LENGTH', 'HTTP_AUTHORIZATION',
                     'HTTP_HOST', 'HTTP_USER_AGENT', 'HTTP_X_FORWARDED_FOR', 'HTTP_X_REAL_IP', ' HTTP_X_REQUEST_ID']
        result = dict(
            method=self.request.method,
            meta={key.lower(): str(value) for key, value in self.request.META.items() if key in meta_keys},
            path=self.request.path_info,
            scheme=self.request.scheme
        )
        try:
            result['data'] = {key: value for key, value in self.request.data.items()}
        except AttributeError:
            if self.request.method == 'GET':
                result['data'] = self.request.GET.dict()
            elif self.request.method == 'POST':
                result['data'] = self.request.POST.dict()

        try:
            result['user'] = str(self.request.user)
        except AttributeError:
            result['user'] = None

        return result

    def format_response(self):
        result = dict(
            status=self.response.status_code,
            reason=self.response.reason_phrase,
            headers=dict(self.response.items()),
            charset=self.response.charset,
            content=self.response.content.decode(),
        )
        if settings.LOG_RESPONSE_JSON_ONLY and 'application/json' not in self.response['Content-Type']:
            result['content'] = ''
        return result
