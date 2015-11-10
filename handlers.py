import json
import sys
from datetime import datetime
from .log_object import LogObject
from logging import FileHandler, StreamHandler
from . import settings


class DLFileHandler(FileHandler):
    def emit(self, record):
        return super().emit(record)

    def format(self, record):
        if not isinstance(record.msg, LogObject):
            return super().format(record)

        message = record.msg.to_dict

        formatted = dict()
        for field in settings.INFO_FIELDS:
            if field == 'datetime':
                formatted[field] = datetime.fromtimestamp(record.created).isoformat()
            if field == 'method':
                formatted[field] = message['request']['method']
            if field == 'path':
                formatted[field] = message['request']['path']
            if field == 'request_type':
                formatted[field] = message['request']['meta']['content_type']
            if field == 'request_length':
                formatted[field] = message['request']['meta']['content_length']
            if field == 'response_status':
                formatted[field] = message['response']['status']
            if field == 'response_reason':
                formatted[field] = message['response']['reason']

        if settings.FORMAT.lower() == 'json':
            return json.dumps(formatted)
        else:
            return ' '.join(str(v) for v in formatted.values())


class ConsoleHandler(StreamHandler):
    def emit(self, record):
        return super().emit(record)

    def format(self, record):
        if not isinstance(record.msg, LogObject):
            return super().format(record)

        return json.dumps(record.msg.to_dict)
