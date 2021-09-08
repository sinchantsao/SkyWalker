# coding=utf8

import typing as t
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session
from X4._stock_info import TradingDates, db_engine


def get_previous_trade_date(cur_trade_date: str) -> t.Union[str, None]:
    db_session: Session = sessionmaker(db_engine)()
    trade_date = db_session.query(TradingDates) \
                           .filter(TradingDates.cal_date == cur_trade_date) \
                           .one_or_none()
    db_session.close()
    if trade_date is None:
        return None
    return trade_date.pretrade_date


def get_past_trade_dates(cur_trade_date: str, interval: int):
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(TradingDates.cal_date) \
                              .filter(TradingDates.cal_date < cur_trade_date) \
                              .filter(TradingDates.is_open == 1)
    trade_dates = result.all()
    return [td[0] for td in trade_dates[-interval:]]


def get_past_trade_date(cur_trade_date: str, interval: int):
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(TradingDates.cal_date) \
                              .filter(TradingDates.cal_date < cur_trade_date) \
                              .filter(TradingDates.is_open == 1)
    trade_dates = result.all()
    try:
        return trade_dates[-interval][0]
    except IndexError:
        return None


def get_next_trade_date(cur_trade_date: str) -> t.Union[str, None]:
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
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(TradingDates.cal_date) \
                              .filter(TradingDates.cal_date > cur_trade_date) \
                              .filter(TradingDates.is_open == 1)
    trade_dates = result.all()
    db_session.close()
    return [td[0] for td in trade_dates[:interval]]

def get_future_trade_date(cur_trade_date: str, interval: int) -> t.Union[str, None]:
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
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(TradingDates.cal_date) \
                              .filter(TradingDates.cal_date >= start_date) \
                              .filter(TradingDates.cal_date <= end_date) \
                              .filter(TradingDates.is_open == 1)
    trade_dates = result.all()
    db_session.close()
    return [td[0] for td in trade_dates]


