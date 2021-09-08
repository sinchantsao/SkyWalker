# coding=utf8
__author__ = 'caoxingcheng'

import chardet
import logging
from typing import BinaryIO
from six import string_types

logger = logging.getLogger(__name__)


def get_coding(chars):
    u"""
    对于数据量较大字符最好通过该方法获取到对应的编码信息
    相对于unity_string函数的定制处理并不完善,先可以通过UniversalDetector工具类对数据进行训练得到编码,
    字符数据较小(仅几个字符或一行简短的数据)则可以直接使用unity_string函数
    """
    detector = chardet.universaldetector.UniversalDetector()
    if isinstance(chars, (BinaryIO, list)):
        for line in chars:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        return detector.result['encoding']
    detector.feed(chars)
    detector.close()
    return detector.result['encoding']


def convert_to_unicode(content, encode=None, decode=None):
    u"""
    为了统一编码, 在数据处理过程中尽可能统一采用unicode字符处理,
    该方法将数据均处理成unicode字符,chardet模块识别置信度根据实际情况调整,
    对于未知编码尽可能考虑采用GB18030中文拓展字符编码
    可以结合getCoding函数使用,获取更精确的编码信息进行编码处理
    """
    try:
        if isinstance(content, string_types):
            if decode is not None:
                content = content.encode(encode or "GB18030").decode(decode)
        elif encode is not None:
            content = string_types(content, encode)
        else:
            detectReport = chardet.detect(content)
            encodeTyp = detectReport["encoding"]
            confidence = detectReport["confidence"]
            language = detectReport["language"]
            if encodeTyp is not None:
                if encodeTyp in ('ISO-8859-1', 'KOI8-R', 'IBM855'):
                    encodeTyp = "GB18030"
                elif confidence < 0.95:
                    encodeTyp = "GB18030"
            elif language in ('Thai', 'Russia'):
                encodeTyp = "GB18030"
            else:
                encodeTyp = "GB18030"
            content = content.decode(encodeTyp)
    except UnicodeDecodeError as e:
        content = content.decode('GB18030', errors='replace')
    return content
