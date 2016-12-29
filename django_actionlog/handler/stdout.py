# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

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
            print(output)
        else:
            if 'ex_type' in messages:
                output = log_format.error_log(messages)
            else:
                output = log_format.standard_log(messages)
            print(output)

handler_manager.register('stdout', Stdout)
