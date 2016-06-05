# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from . import handler_manager
from . import log_format


class File(object):
    """
    Output to File
    """
    def __init__(self, config):
        self.logfile = config['logfile'] if config.get('logfile') else '/tmp/django_action.log'

    def emit(self, messages):
        if not messages.get('is_middleware'):
            output = log_format.dict_to_str(messages)
            self.write_to_file(output)
        else:
            if messages['status_code'] == 200:
                output = log_format.status_log_200(messages)
            else:
                output = log_format.status_log_500(messages)
            self.write_to_file(output)

    def write_to_file(self, output):
        with open(self.logfile, 'a') as f:
            f.write(output.encode('utf8'))

handler_manager.register('file', File)
