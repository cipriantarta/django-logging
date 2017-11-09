import logging
from threading import Thread
from time import time
from django.db.backends.utils import CursorWrapper

from .log_object import SqlLogObject, settings
log = logging.getLogger('dl_logger')


class CursorLogWrapper(CursorWrapper):
    def execute(self, sql, params=None):
        return self.log_query(super(CursorLogWrapper, self).execute, sql, params)

    def executemany(self, sql, param_list):
        return self.log_query(super(CursorLogWrapper, self).executemany, sql, param_list)

    def log_query(self, method, *args):
        start = time()
        try:
            return method(*args)
        finally:
            stop = time()
            duration = stop - start

            def do_log(cursor, *log_args):
                if duration < settings.SQL_THRESHOLD:
                    return
                sql = self.db.ops.last_executed_query(cursor, *log_args)
                sql_info = {
                    'sql': sql,
                    'time': "%.3f" % duration
                }
                self.db.queries_log.append(sql_info)
                record = SqlLogObject(sql_info)
                log.info(record)
            Thread(target=do_log, args=(self.cursor, *args)).start()
