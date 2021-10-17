# coding=utf8

import calendar
import datetime
import typing as t
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import func
from X4._stock_info import TradingDates, db_engine
from X4.date import DateStdFmt, Weekday


def get_previous_trade_date(cur_trade_date: str) -> t.Union[str, None]:
    """
    获取前一个交易日日期
    Args:
        cur_trade_date: 需要预算的基准日期, 格式: %Y%m%d

    Returns: 前一个交易日日期, 格式: %Y%m%d
    """
    db_session: Session = sessionmaker(db_engine)()
    trade_date = db_session.query(TradingDates) \
                           .filter(TradingDates.cal_date == cur_trade_date) \
                           .one_or_none()
    db_session.close()
    if trade_date is None:
        return None
    return trade_date.pretrade_date


def get_past_trade_dates(cur_trade_date: str, interval: int) -> t.List:
    """
    获取过去 n 个交易日日期数据
    Args:
        cur_trade_date: 需要预算的基准日期, 格式: %Y%m%d
        interval: 基准日期的前 n 个交易日期数

    Returns: 过去 n 个交易日日期数据

    """
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(TradingDates.cal_date) \
                              .filter(TradingDates.cal_date < cur_trade_date) \
                              .filter(TradingDates.is_open == 1)
    trade_dates = result.all()
    db_session.close()
    return [td[0] for td in trade_dates[-interval:]]


def get_past_trade_date(cur_trade_date: str, interval: int) -> t.Union[str, None]:
    """
    获取过去第 n 个交易日日期
    Args:
        cur_trade_date: 需要预算的基准日期, 格式: %Y%m%d
        interval: 过去第 n 个交易日日期数

    Returns: 过去第 n 个交易日日期, 格式: %Y%m%d
    """
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(TradingDates.cal_date) \
                              .filter(TradingDates.cal_date < cur_trade_date) \
                              .filter(TradingDates.is_open == 1)
    trade_dates = result.all()
    db_session.close()
    try:
        return trade_dates[-interval][0]
    except IndexError:
        return None


def get_next_trade_date(cur_trade_date: str) -> t.Union[str, None]:
    """
    获取下一个交易日日期
    Args:
        cur_trade_date: 需要预算的基准日期, 格式: %Y%m%d

    Returns: 下一个交易日日期, 格式: %Y%m%d
    """
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(TradingDates.cal_date) \
                              .filter(TradingDates.cal_date > cur_trade_date) \
                              .filter(TradingDates.is_open == 1) \
                              .order_by(TradingDates.cal_date)
    trade_date = result.first()
    if trade_date is None:
        return trade_date
    return trade_date[0]


def get_future_trade_dates(cur_trade_date: str, interval: int) -> t.List[str]:
    """
    获取未来 n 个交易日日期
    Args:
        cur_trade_date: 需要预算的基准日期数据, 格式: %Y%m%d
        interval: 未来 n 个交易日数

    Returns: 未来 n 个交易日日期
    """
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(TradingDates.cal_date) \
                              .filter(TradingDates.cal_date > cur_trade_date) \
                              .filter(TradingDates.is_open == 1)
    trade_dates = result.all()
    db_session.close()
    return [td[0] for td in trade_dates[:interval]]


def get_future_trade_date(cur_trade_date: str, interval: int) -> t.Union[str, None]:
    """
    获取未来第 n 个交易日日期
    Args:
        cur_trade_date: 需要预算的基准日期, 格式: %Y%m%d
        interval: 未来第 n 个交易日数

    Returns: 未来第 n 个交易日日期
    """
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(TradingDates.cal_date) \
                              .filter(TradingDates.cal_date > cur_trade_date) \
                              .filter(TradingDates.is_open == 1) \
                              .order_by(TradingDates.cal_date)
    trade_dates = result.all()
    db_session.close()
    try:
        return trade_dates[interval-1][0]
    except IndexError:
        return None


def get_trade_date_range(start_date: str, end_date: str) -> t.List[str]:
    """
    获取自然日日期区间内的所有交易日日期
    Args:
        start_date: 起始日期(包含在内)
        end_date: 终止日期(包含在内)

    Returns: 日期区间内的所有交易日日期
    """
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(TradingDates.cal_date) \
                              .filter(TradingDates.cal_date >= start_date) \
                              .filter(TradingDates.cal_date <= end_date) \
                              .filter(TradingDates.is_open == 1)
    trade_dates = result.all()
    db_session.close()
    return [td[0] for td in trade_dates]


def get_month_trade_dates(year: int, month: int) -> t.List[str]:
    """
    获取指定年的指定月的对应月份内的所有交易日
    Args:
        year: 指定年份
        month: 指定月份

    Returns: 传入日期数据对应月份内的所有交易日
    """
    date = datetime.date(year, month, 1)
    date_month_first_weekday, month_end = calendar.monthrange(year=date.year, month=date.month)
    date_month_start = datetime.date(year=date.year, month=date.month, day=1)
    date_month_end = datetime.date(year=date.year, month=date.month, day=month_end)

    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(TradingDates.cal_date) \
                              .filter(TradingDates.is_open == 1) \
                              .filter(TradingDates.cal_date >= date_month_start.strftime(DateStdFmt)) \
                              .filter(TradingDates.cal_date <= date_month_end.strftime(DateStdFmt)) \
                              .order_by(TradingDates.cal_date)
    trade_dates = result.all()
    db_session.close()
    return [d[0] for d in trade_dates]


def get_month_last_trade_date(year: int, month: int) -> str:
    """
    获取指定年的指定月的对应月份内的最后一个交易日
    Args:
        year: 指定年份
        month: 指定月份

    Returns: 指定年的指定月的对应月份内的最后一个交易日
    """
    date = datetime.date(year, month, 1)
    date_month_first_weekday, month_end = calendar.monthrange(year=date.year, month=date.month)
    date_month_start = datetime.date(year=date.year, month=date.month, day=1)
    date_month_end = datetime.date(year=date.year, month=date.month, day=month_end)

    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(func.max(TradingDates.cal_date)) \
                              .filter(TradingDates.is_open == 1) \
                              .filter(TradingDates.cal_date >= date_month_start.strftime(DateStdFmt)) \
                              .filter(TradingDates.cal_date <= date_month_end.strftime(DateStdFmt)) \
                              .order_by(TradingDates.cal_date)
    result = result.one_or_none()
    last_trade_date = result[0] if result else None
    return last_trade_date


def get_week_last_trade_date(cur_date: str) -> str:
    """
    获取基准日期对应星期的最后一个交易日
    Args:
        cur_date: 需要预算的基准日期, 格式: %Y%m%d

    Returns: 基准日期对应星期的最后一个交易日
    """
    date = datetime.datetime.strptime(cur_date, DateStdFmt)
    weekday = date.weekday()
    monday = (date - datetime.timedelta(days=weekday)).strftime(DateStdFmt)
    sunday = (date + datetime.timedelta(days=(Weekday.Sun - weekday))).strftime(DateStdFmt)
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(TradingDates.cal_date) \
                              .filter(TradingDates.cal_date >= monday) \
                              .filter(TradingDates.cal_date <= sunday) \
                              .filter(TradingDates.is_open == 1) \
                              .order_by(TradingDates.cal_date)
    trade_dates = result.all()
    if trade_dates:
        last_trade_date = trade_dates[-1][0]
    else:
        last_trade_date = None
    return last_trade_date


if __name__ == '__main__':
    print(get_week_last_trade_date("20211027"))


