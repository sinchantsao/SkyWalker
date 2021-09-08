# coding=utf8

""" 出现此类错误多是没有按照框架开发标准 """

from . import _CodeNumException


class StandError(_CodeNumException):
    def __init__(self, *args, **kwargs):
        super(StandError, self).__init__(1000, *args, **kwargs)


class ParamStandError(StandError):
    def __init__(self, *args, **kwargs):
        super(ParamStandError, self).__init__(1001, *args, **kwargs)


class ArgStandError(StandError):
    def __init__(self, *args, **kwargs):
        super(ArgStandError, self).__init__(1002, *args, **kwargs)


class MethodStandError(StandError):
    def __init__(self, *args, **kwargs):
        super(MethodStandError, self).__init__(1003, *args, **kwargs)


class IllegalOperationError(StandError):
    """ 使用不当 """
    def __init__(self, *args, **kwargs):
        super(IllegalOperationError, self).__init__(1003, *args, **kwargs)
