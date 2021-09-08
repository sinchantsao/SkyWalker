# coding=utf8

import typing as t
from enum import Enum
from os import path
from pandas import Series
from X2.XDB.sql.connections import LocalStorage
from X1.support import SysSupport
from X4.utils import clean_stock_name
from X4 import fields

class FeeType(Enum):
    checked = 0
    over = 1
    under = 2


def check_transfer_fee(record: t.Union[dict, Series], fee_rate: float) -> FeeType:
    try:
        stock_code = record[fields.StockCode]
    except KeyError:
        stock_name = record[fields.StockName]
        stock_name = clean_stock_name(stock_name)
        stock_codes = LocalStorage(path.abspath(__file__))\
            .execute(sql="SELECT stock_code FROM stock_info;",
                     values=(),
                     fetchall=True,
                     onecol=True)
        if not stock_codes:
            raise SysSupport(f"Stock table contains no info for `{stock_name}`")

    pass
