# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time

from django.core.urlresolvers import resolve, Resolver404

try:
    from django.conf import settings
    ACTION_LOG_SETTING = settings.ACTION_LOG_SETTING
except AttributeError:
    ACTION_LOG_SETTING = {'handler_type': 'null'}

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from .sql_logger import SqlLogger, ready_sql_logger
from .actionlog import ActionLog

_action_log = ActionLog(ACTION_LOG_SETTING, is_middleware=True)
_is_enable = True if ACTION_LOG_SETTING['handler_type'] != 'null' else False


class ActionLogMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if _is_enable:
            request.actionlog_start = time.time()
            request.sql_logger = SqlLogger()
            ready_sql_logger(request.sql_logger)

    def process_response(self, request, response):
        if not hasattr(request, 'actionlog_start'):
            return response

        message = self._create_log_message(request)
        message['status_code'] = response.status_code

        sql_logger = request.sql_logger
        message['sql_count'] = sql_logger.sql_count
        message['sql_time'] = sql_logger.sql_time
        message['python_time'] = round((message['total_time'] - sql_logger.sql_time), 2)
        _action_log.log(**message)
        return response

    def process_exception(self, request, ex):
        if not hasattr(request, 'actionlog_start'):
            return

        message = self._create_log_message(request)
        message['status_code'] = 500
        message['ex_type'] = ex.__class__.__name__
        message['ex_message'] = unicode(ex.message)
        _action_log.log(**message)

    def _create_log_message(self, request):
        path = request.path
        try:
            view_name = resolve(path).view_name
        except Resolver404:
            view_name = '{}'.format(path)

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
                   'request_id': id(request),
                   'view_name': view_name,
                   'method': request.method,
                   'user': user_name,
                   'total_time': round((time.time() - request.actionlog_start), 2)}
        return message
