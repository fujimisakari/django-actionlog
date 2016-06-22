# -*- coding: utf-8 -*-

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = __import__('django_actionlog').__version__

setup(
    name='django-actionlog',
    version=version,
    description="You can check the python-time, sql-time and query-count for each request for Django",
    long_description=read('README.rst'),
    author='Ryo Fujimoto',
    author_email='fujimisakari@gmail.com',
    url='http://github.com/fujimisakari/django-actionlog',
    license='BSD',
    packages=['django_actionlog', 'django_actionlog.handler'],
    install_requires=['fluent-logger'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
)
