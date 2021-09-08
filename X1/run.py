# coding=utf8

""" 出现此类错误都是由于没有考虑到的、没有遇到过的情景 """

from . import _CodeNumException


class UnexpectedCompatible(_CodeNumException):
    def __init__(self, *args, **kwargs):
        super(UnexpectedCompatible, self).__init__(5002, *args, **kwargs)


class UnexpectedData(_CodeNumException):
    def __init__(self, *args, **kwargs):
        super(UnexpectedData, self).__init__(5003, *args, **kwargs)


class UnexpectedFile(_CodeNumException):
    def __init__(self, *args, **kwargs):
        super(UnexpectedFile, self).__init__(5004, *args, **kwargs)


class UndevelopedFile(_CodeNumException):
    def __init__(self, *args, **kwargs):
        super(UndevelopedFile, self).__init__(5005, *args, **kwargs)


class RetryException(_CodeNumException):
    def __init__(self, *args, **kwargs):
        super(RetryException, self).__init__(5100, *args, **kwargs)
