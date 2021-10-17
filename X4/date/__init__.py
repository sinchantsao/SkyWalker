# coding=utf8

import calendar
import datetime
import re
import typing as t
from enum import IntEnum
from X1.run import UnexpectedData

DateStdFmt = "%Y%m%d"
TimeStdFmt = "%Y-%m-%d %H:%M:%S"


def century_from_year(year: int) -> int:
    """
    获取年份对应的世纪
    Args:
        year: 指定年份

    Returns: 世纪
    """
    return year // 100 + 1


def match_string_date(string: t.AnyStr, position: int = 0,
                      century: int = century_from_year(datetime.date.today().year),
                      strict: bool = True) -> t.Dict[str, str]:
    """
    用于匹配字符串中的日期数据; (这个函数存在一定缺陷, 不能识别平年闰年, 没想到更好的方法)
    Args:
        string: 需要用于匹配日期数据的字符串数据
        position: 匹配的日期数据可能会有多个, 需要确认需要的是第几个日期数据才是符合需求的
        century: 增加一定准确度, 默认采用当前世纪, 如若是跨世纪日期, 做好相关的应用设计.
        strict: 是否严格遵守4位年数据/2位月数据/2位日数据

    Returns: 返回匹配到的年月日数据,分别 key 为 'year'/'month'/'day' 存放于字典当中;
             当未匹配到数据也会返回同样结构的字段数据, 只是对应的数据均为空字符;
    """
    rules = [
        """
        (?P<year>%s\\d{2})
        (?P<year_sep>[/\\-_\u5e74]?)  # \u5e74 为`年`的 unicode 形式
        (?P<month>0[1-9]|1[0-2])
        (?P<month_sep>[/\\-_\u6708]?)  # \u6708 为`月`的 unicode 形式
        (?P<day>0[1-9]|[12][0-9]|3[01])
        (?P<day_sep>\u65e5?)  # \u65e5 为`日`的 unicode 形式
        """ % (century - 1),
        """
        (?P<year>%s\\d{2})
        (?P<year_sep>[/\\-_\u5e74]?)  # \u5e74 为`年`的 unicode 形式
        (?P<month>[1-9])
        (?P<month_sep>[/\\-_\u6708]?)  # \u6708 为`月`的 unicode 形式
        (?P<day>0[1-9]|[12][0-9]|3[01]|[1-9])
        (?P<day_sep>\u65e5?)  # \u65e5 为`日`的 unicode 形式
        """ % (century - 1)
    ]
    for rule in rules:
        match_regex = re.compile(rule, flags=re.X)
        matched = match_regex.search(string)
        if matched is not None:
            data = matched.groups()
        else:
            continue
        s = position * 6
        e = s + 6
        data = data[s: e]
        if data:
            result = {
                "year": data[0],
                "year_sep": data[1],
                "month": data[2],
                "month_sep": data[3],
                "day": data[4],
                "day_sep": data[5],
            }
            if strict:
                if len(result["year"]) != 4:
                    raise UnexpectedData(f"year data should be a 4-digit but {len(result['year'])}.",
                                         cause_data=(string, result))
                if len(result["month"]) != 2:
                    raise UnexpectedData(f"month data should be a 2-digit but {len(result['month'])}.",
                                         cause_data=(string, result))
                if len(result["day"]) != 2:
                    raise UnexpectedData(f"day data should be a 2-digit but {len(result['day'])}.",
                                         cause_data=(string, result))
            else:
                result["year"] = result["year"].zfill(4)
                result["month"] = result["month"].zfill(2)
                result["day"] = result["day"].zfill(2)
            return result
    else:
        return {"year": '', "month": '', "day": ''}


def convert_date_format(cur_date: str, new_format: str, old_format=DateStdFmt):
    """
    转换日期格式
    Args:
        cur_date: 日期字符串数据
        new_format: 需要转换的新格式
        old_format: 原日期格式, 默认采用框架标准格式: X4.date.DateStdFmt -> %Y%m%d

    Returns: 重新格式化后的日期数据
    """
    date = datetime.datetime.strptime(cur_date, old_format)
    return date.strftime(new_format)


def month_last_date(year: int, month: int) -> str:
    """
    获取指定年的指定月的对应月份最后一天日期
    Args:
        year: 指定年
        month: 指定月

    Returns: 指定年的指定月的对应月份最后一天日期
    """
    cur_date = datetime.date(year, month, 1)
    _, date_range = calendar.monthrange(cur_date.year, cur_date.month)
    last_date = datetime.date(year=cur_date.year, month=cur_date.month, day=date_range)
    return last_date.strftime(DateStdFmt)


class Weekday(IntEnum):
    Mon = 0
    Tue = 1
    Wed = 2
    Thu = 3
    Fri = 4
    Sat = 5
    Sun = 6
    __DAYS__ = 7


def get_last_weekday(date: str, weekday: t.Union[int, Weekday]):
    """
    获取上周星期x的日期
    Args:
        date: 需要预算的基准日期, 格式: %Y%m%d
        weekday: 星期信息, 如果采用 int 数据请以 python 星期标准使用(周一为 0, 以此类推)

    Returns: 上周星期x的日期
    """
    date = datetime.datetime.strptime(date, DateStdFmt)
    delta = datetime.timedelta(date.weekday() + Weekday.__DAYS__ - weekday)
    last_weekday = date - delta
    return last_weekday.strftime(DateStdFmt)


def get_date_weekday(cur_date: str) -> Weekday:
    """
    获取日期对应的星期信息
    Args:
        cur_date: 需要预算的基准日期, 格式: %Y%m%d

    Returns: 返回的数据为 Weekday 枚举对象, 由于 Weekday 继承于 IntEnum,
             因此返回的 Weekday 对象数据也可以作为 int 数据使用;
    """
    date = datetime.datetime.strptime(cur_date, DateStdFmt)
    return Weekday(date.weekday())
