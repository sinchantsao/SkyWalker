# coding=utf8

import typing as t
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session
from X4._stock_info import StockBasicInfo, db_engine
from X4.utils import _stock_code_check, clean_stock_name


def get_code_market_belong(stock_code: str) -> t.Union[str, None]:
    _stock_code_check(stock_code)
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(StockBasicInfo.market) \
                              .filter(StockBasicInfo.symbol == stock_code)
    data = result.one_or_none()
    if data is None:
        return data
    return data[0]


def get_code_industry_belong(stock_code: str) -> t.Union[str, None]:
    _stock_code_check(stock_code)
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(StockBasicInfo.industry) \
                              .filter(StockBasicInfo.symbol == stock_code)
    data = result.one_or_none()
    if data is None:
        return data
    return data[0]


def get_code_stock_name(stock_code: str) -> t.Union[str, None]:
    _stock_code_check(stock_code)
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(StockBasicInfo.name) \
        .filter(StockBasicInfo.symbol == stock_code)
    data = result.one_or_none()
    if data is None:
        return data
    return data[0]


def get_stock_name_code(stock_name: str) -> t.Union[str, None,]:
    stock_name = clean_stock_name(stock_name)
    db_session: Session = sessionmaker(db_engine)()
    result: Query = db_session.query(StockBasicInfo.symbol) \
                              .filter(StockBasicInfo.name == stock_name)
    data = result.one_or_none()
    if data is None:
        return data
    return data[0]

