# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime


OUTPUT_STANDARD = '================== Footprint Log ==================\n' \
                  'time        : {}\n' \
                  'url         : {}\n' \
                  'view_name   : {}\n' \
                  'request_id  : {}\n' \
                  'status_code : {}\n' \
                  'method      : {}\n' \
                  'user        : {}\n' \
                  'remote_ip   : {}\n' \
                  'user_agnet  : {}\n' \
                  'sql_count   : {}\n' \
                  'sql_time    : {}\n' \
                  'python_time : {}\n' \
                  'total_time  : {}\n\n'


OUTPUT_ERROR = '================== Footprint Log ==================\n' \
               'time        : {}\n' \
               'url         : {}\n' \
               'view_name   : {}\n' \
               'status_code : {}\n' \
               'method      : {}\n' \
               'user        : {}\n' \
               'remote_ip   : {}\n' \
               'user_agnet  : {}\n' \
               'ex_type     : {}\n' \
               'ex_message  : {}\n\n'


def _get_time_str():
    return datetime.datetime.now().strftime(u'%Y/%m/%d %H:%M:%S')


def standard_log(messages):
    output = OUTPUT_STANDARD.format(_get_time_str(),
                                    messages['url'],
                                    messages['view_name'],
                                    messages['request_id'],
                                    messages['status_code'],
                                    messages['method'],
                                    messages['user'],
                                    messages['remote_ip'],
                                    messages['user_agent'],
                                    messages['sql_count'],
                                    messages['sql_time'],
                                    messages['python_time'],
                                    messages['total_time'])
    return output


def error_log(messages):
    output = OUTPUT_ERROR.format(_get_time_str(),
                                 messages['url'],
                                 messages['view_name'],
                                 messages['status_code'],
                                 messages['method'],
                                 messages['user'],
                                 messages['remote_ip'],
                                 messages['user_agent'],
                                 messages['ex_type'],
                                 messages['ex_message'])
    return output


def dict_to_str(messages):
    """
    :param dict messages: {'fizz': 'buzz', ...}
    :rtype: str
    """
    def get_max_length(msg_key_list, max_length=4):
        if msg_key_list:
            max_length = max_length if max_length >= len(msg_key_list[0]) else len(msg_key_list[0])
            return get_max_length(msg_key_list[1:], max_length)
        else:
            return max_length
    del messages['is_middleware']
    max_length = get_max_length(tuple(messages)) + 1
    output = '\n------------------ Action Log ------------------\n'
    output += '{: <{}}: {}\n'.format('time', max_length, _get_time_str())
    for key, val in messages.items():
        output += '{: <{}}: {}\n'.format(key, max_length, val)
    output += '\n'
    return output
