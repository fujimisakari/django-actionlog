# -*- coding: utf-8 -*-

try:
    from django.conf import settings
    ACTION_LOG_SETTING = settings.ACTION_LOG_SETTING
except AttributeError:
    ACTION_LOG_SETTING = {'handler_type': 'null', 'logfile': '/tmp/django_action.log'}

from .handler import handler_manager


class ActionLog(object):

    def __init__(self, config, is_middleware=False):
        self._output = handler_manager.get(config['handler_type'])(config)
        self._is_middleware = is_middleware

    def log(self, **kwargs):
        """
        Output Log
        """
        record = dict(kwargs)
        record.update({'is_middleware': self._is_middleware})
        self._output.emit(record)


def output(messages):
    actlog = ActionLog(ACTION_LOG_SETTING)
    actlog.log(**messages)
