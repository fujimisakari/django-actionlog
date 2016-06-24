# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime


OUTPUT_200 = '================== Footprint Log ==================\n' \
             'time        : {}\n' \
             'url         : {}\n' \
             'view_name   : {}\n' \
             'status_code : {}\n' \
             'method      : {}\n' \
             'user        : {}\n' \
             'sql_count   : {}\n' \
             'sql_time    : {}\n' \
             'python_time : {}\n' \
             'total_time  : {}\n\n'


OUTPUT_500 = '================== Footprint Log ==================\n' \
             'time        : {}\n' \
             'url         : {}\n' \
             'view_name   : {}\n' \
             'status_code : {}\n' \
             'method      : {}\n' \
             'user        : {}\n' \
             'ex_type     : {}\n' \
             'ex_message  : {}\n\n'


def _get_time_str():
    return datetime.datetime.now().strftime(u'%Y/%m/%d %H:%M:%S')


def status_log_200(messages):
    output = OUTPUT_200.format(_get_time_str(),
                               messages['url'],
                               messages['view_name'],
                               messages['status_code'],
                               messages['method'],
                               messages['user'],
                               messages['sql_count'],
                               messages['sql_time'],
                               messages['python_time'],
                               messages['total_time'])
    return output


def status_log_500(messages):
    output = OUTPUT_500.format(_get_time_str(),
                               messages['url'],
                               messages['view_name'],
                               messages['status_code'],
                               messages['method'],
                               messages['user'],
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
