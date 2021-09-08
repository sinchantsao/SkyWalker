# coding=utf8

import re
from enum import Enum
from typing import Tuple
from X1.stand import ArgStandError
from X1.run import UnexpectedData


class StockData(Enum):
    trade_account = 1
    trade_date = 2
    total_asset = 3
    netvalue = 4
    total_marketvalue = 5
    fund_balance = 6
    total_liabilities = 7
    bonds_liabilities = 8
    financed_liabilities = 9
    trade_flow = 10
    stock_position = 11
    contract_position = 12


class FileType(Enum):
    Excel = 1
    CSV = 2
    TXT = 3
    PDF = 4


class FileAttribution(Enum):
    Mainland = 1
    CICC = 2
    UBS = 3


# 对于txt文本类文件数据, 为了统一管理, 必须通过正则表达式形式进行匹配数据;
# 为了更好的获取到匹配数据,每一个匹配到的数据都必须带上名称(组名);
# 以下是对于每一类数据正则匹配限制的命名;
DestinationGroups: [StockData, Tuple[str]] = {
    StockData.trade_account:
        ("trade_account",),
    StockData.trade_date:
        ("trade_date",),
    StockData.total_asset:
        ("total_asset",),
    StockData.netvalue:
        ("netvalue",),
    StockData.total_marketvalue:
        ("total_marketvalue",),
    StockData.fund_balance:
        ("fund_balance",),
    StockData.total_liabilities:
        ("total_liabilities",),
    StockData.bonds_liabilities:
        ("bonds_liabilities",),
    StockData.financed_liabilities:
        ("financed_liabilities",),
    StockData.stock_position:
        ("stock_code",
         "stock_name",
         "marketvalue",
         "marketprice",
         "pnl",
         "amount"),
    StockData.trade_flow:
        ("trade_date",
         "event",
         "stock_code",
         "stock_name",
         "volume",
         "price",
         "quantities",
         "balance",
         "brokerage_fee",
         "transfer_fee",
         "service_charge",
         "stamp_tax",
         "remarks"),
    StockData.contract_position:
        ("contract_date",
         "stock_code",
         "stock_name",
         "contract_type",
         "fund_paying",
         "fee_paying",
         "amount",
         "paying",
         "return_date"),
}


class _Column:
    def __init__(self, *,
                 cn: str,
                 eng: str,
                 dtype: type,
                 description: str = None,
                 alias: str = None):
        self.cn = cn
        self.eng = eng
        self.dtype = dtype
        self.description = description
        self.alias = alias

    def __str__(self):
        return self.cn

    def __repr__(self):
        return self.eng

    def adapt(self, value):
        raise NotImplemented


class FloatColumn(_Column):
    def __init__(self, **kwargs):
        super().__init__(dtype=float, **kwargs)

    def adapt(self, value):
        value = re.sub("[()（）,]", repl="", string=str(value))
        return self.dtype(value)


class StringColumn(_Column):
    def __init__(self,  **kwargs):
        super().__init__(dtype=str, **kwargs)

    def adapt(self, value):
        return self.dtype(value)

class BreakingColumn(_Column):
    def __init__(self, breaking_rule, **kwargs):
        """
        用于需要分割数据的列,一列当中存在多种数据,需要分割成多列

        Args:
            breaking_rule: 分割的正则表达式规则,这是一个二元组数据;第一个元素是组名元组数据;
                           第二个元素是带有组名的正则表达式,且包含第一个元素中所有组名.
            **kwargs:
        """
        super().__init__(dtype=str, **kwargs)
        if not (isinstance(breaking_rule, tuple) and
                len(breaking_rule) == 2 and
                isinstance(breaking_rule[0], tuple)):
            raise ArgStandError("breaking_rule should be a tuple with 2 elements, refer to doc.")

    @staticmethod
    def breaking(breaking_rule, value):
        try:
            result = re.search(breaking_rule[1], value).groupdict()
            data = {}
            for ele in breaking_rule[0]:
                data[ele] = result[ele]
        except AttributeError:
            raise UnexpectedData("Can not break out data correctly by regex.", cause_data=value)
        except KeyError:
            raise ArgStandError("Group names do not matched regex groups probably, "
                                "can not match suitable data from regex search result.")
        return data


class StockPosColumns:
    stock_code = StringColumn(cn="证券代码", eng="stock code")
    stock_name = StringColumn(cn="证券名称", eng="stock name")
    marketvalue = FloatColumn(cn="市值", eng="marketvalue")
    marketprice = FloatColumn(cn="市价", eng="marketprice")
    pnl = FloatColumn(cn="收益", eng="pnl")
    amount = FloatColumn(cn="持仓数", eng="pnl")


class TradingFlowColumns:
    trade_date = StringColumn(cn="发生日期", eng="trade date")
    event = StringColumn(cn="交易事件", eng="event")
    stock_code = StringColumn(cn="证券代码", eng="stock code")
    stock_name = StringColumn(cn="证券名称", eng="stock name")
    volume = FloatColumn(cn="成交股数", eng="volume")
    price = FloatColumn(cn="成交价格", eng="price")
    quantities = FloatColumn(cn="发生金额", eng="quantities")
    balance = FloatColumn(cn="资金余额", eng="balance")
    brokerage_fee = FloatColumn(cn="佣金", eng="brokerage fee")
    transfer_fee = FloatColumn(cn="过户费", eng="transfer fee")
    service_charge = FloatColumn(cn="手续费", eng="service charge")
    stamp_tax = FloatColumn(cn="印花税", eng="stamp tax")
    remarks = StringColumn(cn="备注", eng="remarks")


class ContractFlowColumns:
    contract_date = StringColumn(cn="合约日期", eng="contract date")
    stock_code = StringColumn(cn="证券代码", eng="stock code")
    stock_name = StringColumn(cn="证券名称", eng="stock name")
    contract_type = StringColumn(cn="合约类型", eng="contract type")
    fund_paying = FloatColumn(cn="未了结合约金额", eng="fund paying")
    fee_paying = FloatColumn(cn="未了结合约费用", eng="fee paying")
    amount = FloatColumn(cn="未了结合约数量", eng="amount")
    paying = FloatColumn(cn="未了结费用", eng="paying")
    return_date = StringColumn(cn="归还截止日", eng="return date")


