# coding: utf-8

from fluent import event
from fluent import sender

from . import handler_manager


class Fluentd(object):
    """
    Output Fluentd
    """
    def __init__(self, config):
        host = config.get('host', 'localhost')
        port = config.get('port', 24224)
        tag_name = config.get('tag_name', 'django.actionlog')
        sender.setup(tag_name, host=host, port=port)

    def emit(self, messages):
        is_middleware = messages['is_middleware']
        del messages['is_middleware']

        if is_middleware:
            event.Event('footprint', messages)
        else:
            label_name = ''
            if messages.get('label_name'):
                label_name = messages.get('label_name')
                del messages['label_name']
            event.Event(label_name, messages)

handler_manager.register('fluentd', Fluentd)
