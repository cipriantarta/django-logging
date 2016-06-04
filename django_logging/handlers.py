import datetime
import json
import gzip
import time
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from . import settings
from .log_object import LogObject, ErrorLogObject, SqlLogObject
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError


def send_to_elasticsearch(index, timestamp, level, message):
    if settings.ELASTICSEARCH_ENABLED:
        connection = Elasticsearch(hosts=settings.ELASTICSEARCH_HOSTS)
        try:
            connection.index(
                index="{}-{}".format(index, time.strftime('%Y.%m.%d')),
                doc_type="log_object",
                body={
                    "date": datetime.datetime.fromtimestamp(timestamp).isoformat(),
                    "level": level,
                    "message": message
                })
        except ConnectionError:
            pass
        

class AppFileHandler(RotatingFileHandler):
    def emit(self, record):
        if not isinstance(record.msg, LogObject)\
                and not isinstance(record.msg, ErrorLogObject)\
                and not isinstance(record.msg, dict):
            return
        return super(AppFileHandler, self).emit(record)

    def format(self, record):
        created = int(record.created)
        message = record.msg if isinstance(record.msg, dict) else record.msg.to_dict
        data = {record.levelname: {created: message}}
        send_to_elasticsearch("django-logging-app", created, record.levelname, message)
        return json.dumps(data, sort_keys=True)

    def rotation_filename(self, default_name):
        return '{}-{}.gz'.format(default_name, time.strftime('%Y%m%d'))

    def rotate(self, source, dest):
        with open(source, 'rb+') as fh_in:
            with gzip.open(dest, 'wb') as fh_out:
                fh_out.writelines(fh_in)
            fh_in.seek(0)
            fh_in.truncate()


class DebugFileHandler(RotatingFileHandler):
    def emit(self, record):
        if not isinstance(record.msg, LogObject) and \
                not isinstance(record.msg, ErrorLogObject)\
                and not isinstance(record.msg, dict):
            return super(DebugFileHandler, self).emit(record)

    def format(self, record):
        created = int(record.created)
        message = record.msg if isinstance(record.msg, dict) else record.msg.to_dict
        data = {record.levelname: {created: message}}
        return json.dumps(data, sort_keys=True)

    def rotation_filename(self, default_name):
        return '{}-{}.gz'.format(default_name, time.strftime('%Y%m%d'))

    def rotate(self, source, dest):
        with open(source, 'rb+') as fh_in:
            with gzip.open(dest, 'wb') as fh_out:
                fh_out.writelines(fh_in)
            fh_in.seek(0)
            fh_in.truncate()


class ConsoleHandler(StreamHandler):
    def emit(self, record):
        return super(ConsoleHandler, self).emit(record)

    def format(self, record):
        if isinstance(record.msg, LogObject) or isinstance(record.msg, SqlLogObject):
            created = int(record.created)
            message = {record.levelname: {created: record.msg.to_dict}}

            try:
                indent = int(settings.INDENT_CONSOLE_LOG)
            except (ValueError, TypeError):
                indent = None
            return json.dumps(message,
                              sort_keys=True,
                              indent=indent)
        elif isinstance(record.msg, ErrorLogObject):
            return str(record.msg)
        elif isinstance(record.msg, dict):
            created = int(record.created)
            message = {record.levelname: {created: record.msg}}
            return json.dumps(message, sort_keys=True, indent=2)
        else:
            return super(ConsoleHandler, self).format(record)


class SQLFileHandler(RotatingFileHandler):
    def emit(self, record):
        if not isinstance(record.msg, SqlLogObject):
            return
        return super(SQLFileHandler, self).emit(record)

    def format(self, record):
        created = int(record.created)
        message = {record.levelname: {created: record.msg.to_dict}}
        send_to_elasticsearch("django-logging-sql", created, record.levelname, message)
        return json.dumps(message, sort_keys=True)

    def rotation_filename(self, default_name):
        return '{}-{}.gz'.format(default_name, time.strftime('%Y%m%d'))

    def rotate(self, source, dest):
        with open(source, 'rb+') as fh_in:
            with gzip.open(dest, 'wb') as fh_out:
                fh_out.writelines(fh_in)
            fh_in.seek(0)
            fh_in.truncate()

