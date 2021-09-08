# coding=utf8

""" 出现此类错误应该是系统层面的错误 """

from . import _CodeNumException


class BaseSupport(_CodeNumException):
    def __init__(self, *args, **kwargs):
        super(BaseSupport, self).__init__(3000, *args, **kwargs)


class HardSupport(BaseSupport):
    def __init__(self, *args, **kwargs):
        super(HardSupport, self).__init__(3001, *args, **kwargs)


class OSSupport(BaseSupport):
    def __init__(self, *args, **kwargs):
        super(OSSupport, self).__init__(3002, *args, **kwargs)


class SysSupport(BaseSupport):
    def __init__(self, *args, **kwargs):
        super(SysSupport, self).__init__(3003, *args, **kwargs)
