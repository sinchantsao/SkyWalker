# coding=utf8

import typing as t
from decimal import Decimal as D, ROUND_UP


def round(num: t.Union[float, int, str], ndigits=2) -> D:
    """ python 内置 round 函数存在精度问题 """
    return D(num).quantize(D(f".{'0' * (ndigits - 1)}1"), rounding=ROUND_UP)


def str_of_num(num: t.Union[int, float], ndigits: int = 2) -> str:
    """
    将数字转换为 万/亿 为单位的字符串, 未达单位值则保留原样.
    """

    def str_of_size(n, lv):
        if lv >= 2:
            return n, lv
        elif n >= 10000:
            n /= 10000
            lv += 1
            return str_of_size(n, lv)
        else:
            return n, lv

    units = ('', '万', '亿')
    num, level = str_of_size(num, 0)
    if level > len(units):
        level -= 1
    return '{number}{unit}'.format(number=round(num, ndigits), unit=units[level])


