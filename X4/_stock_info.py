# coding=utf8

import logging
import os
import pandas
import sqlite3
import tushare
import typing as t
import sqlalchemy.engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import schema
from sqlalchemy.sql import sqltypes
from sqlalchemy import create_engine
from X1.stand import ArgStandError

Base = declarative_base()
logger = logging.getLogger(__name__)


class StockBasicInfo(Base):
    __tablename__ = "stock_basic_info"

    ts_code = schema.Column(sqltypes.CHAR(10), primary_key=True, nullable=False)
    symbol = schema.Column(sqltypes.CHAR(6), nullable=False, unique=True)
    name = schema.Column(sqltypes.VARCHAR(20), nullable=False)
    area = schema.Column(sqltypes.VARCHAR(50), default='')
    industry = schema.Column(sqltypes.VARCHAR(50), default='')
    fullname = schema.Column(sqltypes.VARCHAR(100), default='')
    enname = schema.Column(sqltypes.VARCHAR(100), default='')
    cnspell = schema.Column(sqltypes.CHAR(15), nullable=False)
    market = schema.Column(sqltypes.VARCHAR(15), nullable=False)
    exchange = schema.Column(sqltypes.CHAR(20), nullable=False)
    curr_type = schema.Column(sqltypes.CHAR(20), nullable=False)
    list_status = schema.Column(sqltypes.CHAR(1), nullable=False)
    list_date = schema.Column(sqltypes.CHAR(8), default='')
    delist_date = schema.Column(sqltypes.CHAR(8), default='')
    is_hs = schema.Column(sqltypes.CHAR(1), nullable=False)


class TradingDates(Base):
    __tablename__ = "trade_dates"

    exchange = schema.Column(sqltypes.CHAR(20), nullable=False)
    cal_date = schema.Column(sqltypes.CHAR(8), nullable=False)
    is_open = schema.Column(sqltypes.INT, nullable=False)
    pretrade_date = schema.Column(sqltypes.CHAR(8), nullable=True)

    __table_args__ = (
        schema.PrimaryKeyConstraint(exchange, cal_date),
    )

    def __repr__(self):
        return f"<exchange: {self.exchange}; " \
               f"cal_date: {self.cal_date}; " \
               f"is_open: {self.is_open}; " \
               f"pretrade_date: {self.pretrade_date}>" \

    __str__ = __repr__

def stock_info_db_engine():
    data_db = os.path.join(os.path.dirname(__file__), "stock_info.db")
    engine_fmt = f"sqlite:///{data_db}"
    engine = create_engine(engine_fmt)
    return engine


db_engine = stock_info_db_engine()
Base.metadata.create_all(bind=db_engine, checkfirst=True)


def create_tushare_cli() -> tushare.pro.client.DataApi:
    env_var = "TUSHARE_TOKEN"
    token = os.getenv(env_var, None)
    if token is None:
        raise ArgStandError(f"You have to set a token variable named `{env_var}` "
                            "for pulling stock info from TuShare. "
                            "Token refer to https://tushare.pro/user/token .")
    tushare_cli = tushare.pro_api(token)
    return tushare_cli

def pull_stock_basic_info(tushare_cli) -> pandas.DataFrame:
    info = tushare_cli.stock_basic(
        **{
            "ts_code": "",
            "name": "",
            "exchange": "",
            "market": "",
            "is_hs": "",
            "list_status": "",
            "limit": "",
            "offset": ""
        }, fields=[
            "ts_code",
            "symbol",
            "name",
            "area",
            "industry",
            "market",
            "list_date",
            "fullname",
            "enname",
            "cnspell",
            "exchange",
            "curr_type",
            "list_status",
            "delist_date",
            "is_hs"
        ])
    logger.debug("Pull stock basic info from tushare.")
    return info

def pull_trade_dates(tushare_cli: tushare.pro.client.DataApi) -> pandas.DataFrame:
    trading_dates = tushare_cli.trade_cal(**{
        "exchange": "",
        "cal_date": "",
        "start_date": "",
        "end_date": "",
        "is_open": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "exchange",
        "cal_date",
        "is_open",
        "pretrade_date"
    ])
    logger.debug("Pull trade dates from tushare.")
    return trading_dates


def update_stock_basic_info(tushare_cli: tushare.pro.client.DataApi,
                            conn: t.Union[sqlite3.Connection, sqlalchemy.engine.base.Engine]):
    stock_basic_info_table = pull_stock_basic_info(tushare_cli)
    stock_basic_info_table.to_sql(name=StockBasicInfo.__tablename__,
                                  con=conn,
                                  index=False,
                                  if_exists="replace")
    logger.debug("Update stock basic info into local sql db.")


def update_trade_dates(tushare_cli: tushare.pro.client.DataApi,
                       conn: t.Union[sqlite3.Connection, sqlalchemy.engine.base.Engine]):
    trade_dates_table = pull_trade_dates(tushare_cli)
    trade_dates_table.to_sql(name=TradingDates.__tablename__,
                             con=conn, index=False, if_exists="replace")
    logger.debug("Update trade dates into local sql db.")

def main():
    tushare_cli = create_tushare_cli()
    update_stock_basic_info(tushare_cli=tushare_cli, conn=db_engine)
    update_trade_dates(tushare_cli=tushare_cli, conn=db_engine)
