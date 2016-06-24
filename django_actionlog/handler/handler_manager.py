# -*- coding: utf-8 -*-

_MODULE_MAP = {}


def register(name, handler_class):
    global _MODULE_MAP
    _MODULE_MAP[name] = handler_class


def get(module_name):
    __import__('{}.{}'.format(_get_package(__name__), module_name))
    return _MODULE_MAP[module_name]


def _get_package(package_path):
    return '.'.join(package_path.split('.')[:-1])
