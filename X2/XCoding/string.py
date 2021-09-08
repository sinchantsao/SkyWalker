# coding=utf8

from six import binary_type, text_type


def toNumber(string, converter=float, default=None):
    try:
        clnString = str(string).strip()
        default = converter(clnString)
    except (ValueError, Exception):
        pass
    return default


toType = toNumber


def jug2unicode(string):
    # 在py3当中默认字符集就是unicode
    if isinstance(string, binary_type):
        return string.decode('utf8')
    return string


def jug2str(string):
    if isinstance(string, text_type):
        return string.encode('utf8')
    return string


# py2中的str相当于py3中的bytes
jug2bytes = jug2str

