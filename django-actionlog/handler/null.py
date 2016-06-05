# -*- coding: utf-8 -*-

from . import handler_manager


class Nullout(object):

    def __init__(self, config):
        pass

    def emit(self, data):
        pass

handler_manager.register('null', Nullout)
