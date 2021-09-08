# coding=utf8

""" 出现此类错误类似于系统层面错误,但更加具体化某一功能特性 """

from . import _CodeNumException


class NoComponentError(_CodeNumException):
    def __init__(self, *args, **kwargs):
        super(NoComponentError, self).__init__(2000, *args, **kwargs)


class ComponentConnectionError(_CodeNumException):
    def __init__(self, *args, **kwargs):
        super(ComponentConnectionError, self).__init__(2001, *args, **kwargs)


class ComponentFeatureError(_CodeNumException):
    def __init__(self, *args, **kwargs):
        super(ComponentFeatureError, self).__init__(2002, *args, **kwargs)
