# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from . import handler_manager
from . import log_format


class Stdout(object):
    """
    Output Standard Out
    """
    def __init__(self, config):
        pass

    def emit(self, messages):
        if not messages.get('is_middleware'):
            output = log_format.dict_to_str(messages)
            print output
        else:
            if messages['status_code'] == 500:
                output = log_format.error_log(messages)
            else:
                output = log_format.standard_log(messages)
            print output

handler_manager.register('stdout', Stdout)
