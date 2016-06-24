# -*- coding: utf-8 -*-

import time
import json

from django.utils import six
from django.db import connections
from django.utils.encoding import force_text


def ready_sql_logger(sql_logger):
    for connection in connections.all():
        set_custom_cursor(connection, sql_logger)


def set_custom_cursor(connection, logger):
    if not hasattr(connection, 'actionlog_cursor'):
        connection.actionlog_cursor = connection.cursor

    def cursor():
        return CustomCursorWrapper(connection.actionlog_cursor(), connection, logger)

    connection.cursor = cursor


class SqlLogger(object):

    def __init__(self):
        self._sql_time = 0
        self._num_queries = 0
        self._queries = []
        self._databases = {}

    @property
    def sql_count(self):
        return self._num_queries

    @property
    def sql_time(self):
        return round((self._sql_time / 1000), 2)

    def record(self, alias, **kwargs):
        self._queries.append((alias, kwargs))
        if alias not in self._databases:
            self._databases[alias] = {
                'time_spent': kwargs['duration'],
                'num_queries': 1,
            }
        else:
            self._databases[alias]['time_spent'] += kwargs['duration']
            self._databases[alias]['num_queries'] += 1
        self._sql_time += kwargs['duration']
        self._num_queries += 1


class CustomCursorWrapper(object):

    def __init__(self, cursor, db, logger):
        self.cursor = cursor
        self.db = db
        self.logger = logger

    def _quote_expr(self, element):
        if isinstance(element, six.string_types):
            return "'%s'" % force_text(element).replace("'", "''")
        else:
            return repr(element)

    def _quote_params(self, params):
        if not params:
            return params
        if isinstance(params, dict):
            return dict((key, self._quote_expr(value))
                        for key, value in params.items())
        return list(map(self._quote_expr, params))

    def _decode(self, param):
        try:
            return force_text(param, strings_only=True)
        except UnicodeDecodeError:
            return '(encoded string)'

    def _record(self, method, sql, params):
        start_time = time.time()
        try:
            return method(sql, params)
        finally:
            stop_time = time.time()
            duration = (stop_time - start_time) * 1000
            stacktrace = []
            _params = ''
            try:
                _params = json.dumps(list(map(self._decode, params)))
            except Exception:
                pass  # object not JSON serializable

            alias = getattr(self.db, 'alias', 'default')
            conn = self.db.connection
            vendor = getattr(conn, 'vendor', 'unknown')

            params = {
                'vendor': vendor,
                'alias': alias,
                'sql': self.db.ops.last_executed_query(
                    self.cursor, sql, self._quote_params(params)),
                'duration': duration,
                'raw_sql': sql,
                'params': _params,
                'stacktrace': stacktrace,
                'start_time': start_time,
                'stop_time': stop_time,
                'is_select': sql.lower().strip().startswith('select'),
            }
            self.logger.record(**params)

    def execute(self, sql, params=()):
        return self._record(self.cursor.execute, sql, params)

    def __getattr__(self, attr):
        return getattr(self.cursor, attr)

    def __iter__(self):
        return iter(self.cursor)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
