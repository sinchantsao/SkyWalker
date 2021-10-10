# coding=utf8

""" 出现此类错误多是没有按照框架开发标准 """

from X1 import _CodeNumException


class StandError(_CodeNumException):
    """
    标准错误，不合规、不符合文档说明等情况导致的错误，由用户错误使用而导致的错误问题
    """
    def __init__(self, *args, **kwargs):
        super(StandError, self).__init__(1000, *args, **kwargs)


class ParamStandError(StandError):
    """
    传入的参数所导致的错误， 一般出现在使用其他接口调用时，传入参数错误所导致的错误
    """
    def __init__(self, *args, **kwargs):
        super(ParamStandError, self).__init__(1001, *args, **kwargs)


class ArgStandError(StandError):
    """
    参数不符合规定所导致的错误，一般出现于检查数据类型时抛出该异常
    """
    def __init__(self, *args, **kwargs):
        super(ArgStandError, self).__init__(1002, *args, **kwargs)


class MethodStandError(StandError):
    """
    方法使用错误
    """
    def __init__(self, *args, **kwargs):
        super(MethodStandError, self).__init__(1003, *args, **kwargs)


class IllegalOperationError(StandError):
    """
    使用不当导致的错误
    """
    def __init__(self, *args, **kwargs):
        super(IllegalOperationError, self).__init__(1003, *args, **kwargs)
