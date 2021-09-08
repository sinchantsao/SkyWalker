# coding=utf8

""" Exception Classes """


class _CodeNumException(BaseException):

    def __init__(self, code, *args, cause_data=None):
        super(_CodeNumException, self).__init__(*args)
        self.code = code
        self.cause_data = cause_data
