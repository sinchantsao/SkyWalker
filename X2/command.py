# coding=utf8
__author__ = 'caoxingcheng'

__all__ = [
    'BashOrange',
    'BashBlue',
    'BashGreen',
    'BashRed',
    'BashLightBlue',
    'BashCyan',
    'BashLightGreen',
    'BashLightOrange',
    'BashLightRed',
    'BashPurple',
    'WarningMessage',
    'ErrorMessage',
    'SuccessMessage',
]

from six import string_types


class _CMDColor(object):
    COLOUR_NUM = '0'
    _START_COLOR = '\033[%sm'
    _MOD = '{string:%s%s}'
    _END_COLOR = '\033[0m'

    def __init__(self, echo, align='l', width=0):
        # type: (string_types, str, int) -> None
        # if isinstance(echo, string_types):
        #     echo = echo.encode('utf-8')
        self.value = echo
        self.align = align
        self.width = width

        direct = '<' if align == 'l' else '>'
        if width < 0:
            raise ValueError('negative not be allowed.')
        else:
            dz = '' if width == 0 else str(width)
        self._align = direct
        self._width = dz
        self._MOD = (self._MOD % (self._align, self._width)).format(string=self.value)
        self._raw = ''.join([self._START_COLOR % self.COLOUR_NUM, self._MOD, self._END_COLOR])

    def __str__(self):
        return self._raw

    def __radd__(self, other):
        return str(other) + self._raw

    def __add__(self, other):
        return self._raw + str(other)

    def __eq__(self, other):
        return self.value == str(other)

    def __nonzero__(self):
        return bool(self.value)


class BashRed(_CMDColor):
    COLOUR_NUM = '31'


class BashGreen(_CMDColor):
    COLOUR_NUM = '32'


class BashOrange(_CMDColor):
    COLOUR_NUM = '33'


class BashBlue(_CMDColor):
    COLOUR_NUM = '34'


class BashPurple(_CMDColor):
    COLOUR_NUM = '35'


class BashCyan(_CMDColor):
    COLOUR_NUM = '36'


class BashLightRed(_CMDColor):
    COLOUR_NUM = '41'


class BashLightGreen(_CMDColor):
    COLOUR_NUM = '42'


class BashLightOrange(_CMDColor):
    COLOUR_NUM = '43'


class BashLightBlue(_CMDColor):
    COLOUR_NUM = '44'


ErrorMessage = BashRed
WarningMessage = BashOrange
SuccessMessage = BashGreen
