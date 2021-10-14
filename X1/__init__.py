# coding=utf8
""" Exception Classes """

import typing as t


class _CodeNumException(BaseException):

    # 标准的错误信息展示模版
    _ExceptionInfo = "Exception {exp_type} raised, " \
                     "exception code: {exp_code}; " \
                     "cause data: {cause_data}; " \
                     "error info: {error_info}; "

    def __init__(self, code: int, *args, cause_data: t.Any = None):
        super(_CodeNumException, self).__init__(*args)
        self.code = code
        self.cause_data = cause_data

    def __unicode__(self):
        """
        错误信息格式化传入：错误类型、错误代码、导致产生错误的数据、错误信息
        """
        return _CodeNumException._ExceptionInfo.format(
            exp_type=type(self),
            exp_code=self.code,
            cause_data=self.cause_data,
            error_info=None if not self.args else (self.args[0] if self.args.__len__() == 1
                                                   else self.args)
        )

    __str__ = __repr__ = __unicode__
