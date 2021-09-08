# coding=utf8
__author__ = 'caoxingcheng'

NOTSET   = 0
DEBUG    = 10
INFO     = 20
WARNING  = 30
WARN     = WARNING
ERROR    = 40
FATAL    = 50
CRITICAL = FATAL

DEFAULT  = WARNING

LEVEL_NAMES = {
    CRITICAL : 'CRITICAL',
    ERROR : 'ERROR',
    WARNING : 'WARNING',
    DEBUG : 'DEBUG',
    NOTSET : 'NOTSET',
    INFO: 'INFO',
    'INFO': INFO,
    'CRITICAL' : CRITICAL,
    'ERROR' : ERROR,
    'WARN' : WARNING,
    'WARNING' : WARNING,
    'DEBUG' : DEBUG,
    'NOTSET' : NOTSET,
    'DEFAULT': DEFAULT,
    None: 'Undefined'
}

