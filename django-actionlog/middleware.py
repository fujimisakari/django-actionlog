# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time
import threading

from django.core.urlresolvers import resolve, Resolver404

try:
    from django.conf import settings
    ACTION_LOG_SETTING = settings.ACTION_LOG_SETTING
except AttributeError:
    ACTION_LOG_SETTING = {'handler_type': 'null'}

from .sql_logger import SqlLogger, ready_sql_logger
from .actionlog import ActionLog

_memoize_object = threading.local()


def _new(obj_name, factory_obj):
    obj = factory_obj()
    setattr(_memoize_object, obj_name, obj)
    return obj


def _get(obj_name):
    return getattr(_memoize_object, obj_name, None)


class ActionLogMiddleware(object):

    def __init__(self):
        self.sql_logger = None
        self.actlog = ActionLog(ACTION_LOG_SETTING, is_middleware=True)

    def process_view(self, request, view_func, view_args, view_kwargs):
        _new('actionlog_start', time.time)
        _new('sqlloger', SqlLogger)
        ready_sql_logger(_get('sqlloger'))

    def process_response(self, request, response):
        sql_logger = _get('sqlloger')
        if sql_logger:
            message = self._create_log_message(request)
            message['status_code'] = 200
            message['sql_count'] = sql_logger.sql_count
            message['sql_time'] = sql_logger.sql_time
            message['python_time'] = round((message['total_time'] - sql_logger.sql_time), 2)
            self.actlog.log(**message)
        return response

    def process_exception(self, request, ex):
        message = self._create_log_message(request)
        message['status_code'] = 500
        message['ex_type'] = ex.__class__.__name__
        message['ex_message'] = unicode(ex.message)
        self.actlog.log(**message)

    def _create_log_message(self, request):
        path = request.path
        try:
            view_name = resolve(path).view_name
        except Resolver404:
            view_name = '{}'.format(path)

        actionlog_start = _get('actionlog_start')
        total_time = round((time.time() - actionlog_start), 2)

        user_name = ''
        login_obj_name = ACTION_LOG_SETTING.get('login_obj_name', 'user')
        if hasattr(request, login_obj_name):
            login_obj = getattr(request, login_obj_name)
            login_check_func = ACTION_LOG_SETTING.get('login_check_func', 'is_authenticated')
            if getattr(login_obj, login_check_func)():
                if hasattr(login_obj, 'actionlog_name'):
                    user_name = login_obj.actionlog_name
                else:
                    user_name = login_obj.id

        message = {'url': '{}?{}'.format(path, request.GET.urlencode()) if request.GET.urlencode() else path,
                   'view_name': view_name,
                   'method': request.method,
                   'user': user_name,
                   'total_time': total_time}
        return message
