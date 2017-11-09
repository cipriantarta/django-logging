import datetime
import json
import gzip
import time
from logging import StreamHandler, DEBUG
from logging.handlers import RotatingFileHandler
from threading import Thread

from . import settings
from .log_object import LogObject, ErrorLogObject, SqlLogObject
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError


def message_from_record(record):
    if isinstance(record.msg, dict) or isinstance(record.msg, str):
        if settings.DEBUG:
            message = record.msg
        else:
            message = dict(raw=record.msg)
    elif isinstance(record.msg, Exception):
        message = ErrorLogObject.format_exception(record.msg)
    else:
        try:
            message = record.msg.to_dict
        except AttributeError:
            url = "https://github.com/cipriantarta/django-logging/issues"
            return dict(raw="Unable to parse LogObject. Please file in a bug at: %s" % url)
    return message


def send_to_elasticsearch(timestamp, level, message):
    Thread(target=__send_to_es, args=(timestamp, level, message)).start()


def __send_to_es(timestamp, level, message):
    index = settings.ELASTICSEARCH_INDEX
    if settings.ELASTICSEARCH_ENABLED:
        conn = Elasticsearch(hosts=settings.ELASTICSEARCH_HOSTS,
                             use_ssl=settings.ELASTICSEARCH_SSL,
                             http_auth=settings.ELASTICSEARCH_AUTH,
                             verify_certs=settings.ELASTICSEARCH_SSL)
        try:
            message = json.loads(message).get(level).get(str(timestamp))
            conn.index(
                index="{}".format(index),
                doc_type="log_objects",
                body={
                    "date": datetime.datetime.fromtimestamp(timestamp).isoformat(),
                    "level": level,
                    "message": message
                })
        except ConnectionError:
            pass


class DefaultFileHandler(RotatingFileHandler):
    def emit(self, record):
        if isinstance(record.msg, SqlLogObject):
            return
        super(DefaultFileHandler, self).emit(record)
        message = self.format(record)
        send_to_elasticsearch(int(record.created), record.levelname, message)

    def format(self, record):
        created = int(record.created)
        message = message_from_record(record)
        return json.dumps({record.levelname: {created: message}}, sort_keys=True)

    def rotation_filename(self, default_name):
        return '{}-{}.gz'.format(default_name, time.strftime('%Y%m%d'))

    def rotate(self, source, dest):
        with open(source, 'rb+') as fh_in:
            with gzip.open(dest, 'wb') as fh_out:
                fh_out.writelines(fh_in)
            fh_in.seek(0)
            fh_in.truncate()


class DebugFileHandler(DefaultFileHandler):
    def emit(self, record):
        if record.levelno != DEBUG:
            return
        return super(DebugFileHandler, self).emit(record)


class ConsoleHandler(StreamHandler):
    def emit(self, record):
        return super(ConsoleHandler, self).emit(record)

    def format(self, record):
        if isinstance(record.msg, LogObject) or isinstance(record.msg, SqlLogObject):
            created = int(record.created)
            message = {record.levelname: {datetime.datetime.fromtimestamp(created).isoformat(): record.msg.to_dict}}

            try:
                indent = int(settings.INDENT_CONSOLE_LOG)
            except (ValueError, TypeError):
                indent = 1
            import pprint
            message = pprint.pformat(message, indent, 160, compact=True)
            return message
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
        super(SQLFileHandler, self).emit(record)
        message = self.format(record)
        send_to_elasticsearch(int(record.created), record.levelname, message)

    def format(self, record):
        created = int(record.created)
        message = {record.levelname: {created: record.msg.to_dict}}
        return json.dumps(message, sort_keys=True)

    def rotation_filename(self, default_name):
        return '{}-{}.gz'.format(default_name, time.strftime('%Y%m%d'))

    def rotate(self, source, dest):
        with open(source, 'rb+') as fh_in:
            with gzip.open(dest, 'wb') as fh_out:
                fh_out.writelines(fh_in)
            fh_in.seek(0)
            fh_in.truncate()

