import abc
import json
import six
import sys
import traceback

from django.http import HttpResponseServerError
from django.views import debug

from . import settings


@six.add_metaclass(abc.ABCMeta)
class BaseLogObject(object):
    def __init__(self, request):
        self.request = request

    @abc.abstractproperty
    def to_dict(self):
        raise NotImplementedError

    def format_request(self):
        meta_keys = ['PATH_INFO', 'HTTP_X_SCHEME', 'REMOTE_ADDR',
                     'TZ', 'REMOTE_HOST', 'CONTENT_TYPE', 'CONTENT_LENGTH', 'HTTP_AUTHORIZATION',
                     'HTTP_HOST', 'HTTP_USER_AGENT', 'HTTP_X_FORWARDED_FOR', 'HTTP_X_REAL_IP', ' HTTP_X_REQUEST_ID']
        result = dict(
            method=self.request.method,
            meta={key.lower(): str(value) for key, value in self.request.META.items() if key in meta_keys},
            path=self.request.path_info,
        )

        result['scheme'] = getattr(self.request, 'scheme', None)

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


class LogObject(BaseLogObject):
    def __init__(self, request, response):
        super(LogObject, self).__init__(request)
        self.response = response

    @property
    def to_dict(self):
        result = dict(
            request=self.format_request(),
            response=self.format_response()
        )
        return result

    @property
    def content(self):
        return self.response.content.decode(settings.ENCODING)

    def matching_content_type(self, headers):
        return (not settings.CONTENT_TYPES) or \
                (len([t for t in settings.CONTENT_TYPES if t in headers['Content-Type']]) > 0)

    def format_response(self):
        result = dict(
            status  = self.response.status_code,
            headers = dict(self.response.items()),
            reason  = getattr(self.response, 'reason_phrase', None),
            charset = getattr(self.response, 'charset', None)
        )

        if self.matching_content_type(result['headers']):
            if settings.CONTENT_JSON_ONLY:
                try:
                    result['content'] = json.loads(self.content)
                except (ValueError, AttributeError):
                    pass
            else:
                try:
                    result['content'] = self.content
                except AttributeError:
                    pass


        for field in result.copy().keys():
            if field not in settings.RESPONSE_FIELDS:
                del result[field]
        return result


class ErrorLogObject(BaseLogObject):
    def __init__(self, request, exception):
        super(ErrorLogObject, self).__init__(request)
        self.exception = exception
        self.__traceback = None

    @property
    def to_dict(self):
        return dict(
            request=self.format_request(),
            exception=ErrorLogObject.format_exception(self.exception)
        )

    @classmethod
    def format_traceback(cls, tb):
        tb = traceback.extract_tb(tb)
        for i in tb:
            yield {'file': i[0], 'line': i[1], 'method': i[2]}

    @classmethod
    def format_exception(cls, exception):
        result = dict(
            message=str(exception),
            type=cls.exception_type(exception),
            traceback=list()
        )
        if sys.version_info.major >= 3 and sys.version_info.minor >= 5:
            _traceback = traceback.TracebackException.from_exception(exception).exc_traceback
        else:
            _, _, _traceback = traceback.sys.exc_info()

        for line in cls.format_traceback(_traceback):
            result['traceback'].append(line)
        return result

    @property
    def response(self):
        if settings.DEBUG:
            return debug.technical_500_response(self.request, type(self.exception), self.exception, self.__traceback)
        else:
            return HttpResponseServerError(content=b'<h1>Internal Server Error</h1>')

    def __str__(self):
        return 'Traceback (most recent call last):\n{}{}: {}'.format(
            ''.join(traceback.format_tb(self.__traceback)),
            ErrorLogObject.exception_type(self.exception), str(self.exception)
        )

    @classmethod
    def exception_type(cls, exception):
        return str(type(exception)).split('\'')[1]


class SqlLogObject(object):
    def __init__(self, query, using=None):
        self.query = query
        self.using = using

    @property
    def to_dict(self):
        result = dict(
            duration=self.query['time'],
            query=self.query['sql'],
        )
        if self.using is not None:
            result['using'] = self.using
        return result
