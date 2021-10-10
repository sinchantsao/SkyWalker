# coding=utf8

""" 出现此类错误都是由于没有考虑到的、没有遇到过的情景 """

from X1 import _CodeNumException


class UnexpectedCompatible(_CodeNumException):
    """
    不可预期的、未兼容的错误
    """
    def __init__(self, *args, **kwargs):
        super(UnexpectedCompatible, self).__init__(5002, *args, **kwargs)


class UnexpectedData(_CodeNumException):
    """
    不可预期的、未兼容的数据导致的错误
    """
    def __init__(self, *args, **kwargs):
        super(UnexpectedData, self).__init__(5003, *args, **kwargs)


class UnexpectedFile(_CodeNumException):
    """
    不可预期的、未兼容的文件导致的错误
    """
    def __init__(self, *args, **kwargs):
        super(UnexpectedFile, self).__init__(5004, *args, **kwargs)


class RetryException(_CodeNumException):
    """
    运行过程中多次重试运行无果导致的错误
    """
    def __init__(self, *args, **kwargs):
        super(RetryException, self).__init__(5100, *args, **kwargs)
