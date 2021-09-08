
import numpy
import re
from collections import OrderedDict
from functools import wraps

# 未定义
INP_UNDEFINED   = 'undefined'

INP_START_TIME     = 'parse_start_time'
INP_END_TIME       = 'parse_end_time'

INP_PARSERNAME  = 'parser_name'
INP_PARSER_AUTH = 'parser_author'
INP_AUTH_MAIL   = 'parser_author_mail'
INP_FOR_FILE    = 'for_file_type'
INP_FOR_REGION  = 'for_region_type'
INP_CHECK_ITEMS = 'check_items'


class _ClassProperty(object):
    def __init__(self, func_get, func_set=None):
        self.func_get = func_get
        self.func_set = func_set

    def __get__(self, instance, owner):
        if owner is None:
            owner = type(instance)
        return self.func_get.__get__(instance, owner)()

    def __set__(self, instance, value):
        if not self.func_set:
            raise AttributeError("can not set attribute")
        type_ = type(instance)
        return self.func_set.__get__(instance, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.func_set = func
        return self

def _classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return _ClassProperty(func)


class IndexSign(object):
    def __init__(self, init=0):
        self._index = init

    def update_index(self, index):
        self._index = index

    @property
    def index(self):
        return self._index

    def __int__(self):
        return self._index

    def __str__(self):
        return str(self._index)

    __repr__ = __str__


class _BaseParser(object):

    _PARSER_NAME = INP_UNDEFINED  # parser name
    _FOR_TYPE    = INP_UNDEFINED  # excel/csv/text/pdf
    _FOR_REGION  = INP_UNDEFINED  # UBS/CICC/Mainland
    _PARSER_AUTH = INP_UNDEFINED  # coder
    _AUTH_MAIL   = INP_UNDEFINED  # coder email addr

    @_classproperty
    def parsername(cls):
        return cls._PARSER_NAME

    @_classproperty
    def for_file(cls):
        return cls._FOR_TYPE

    @_classproperty
    def for_region(cls):
        return cls._FOR_REGION

    @_classproperty
    def parser_author(cls):
        return cls._PARSER_AUTH

    @_classproperty
    def author_mail(cls):
        return cls._AUTH_MAIL

    @_classproperty
    def parser_info(cls):
        return {
            INP_PARSERNAME  : cls.parsername,
            INP_PARSER_AUTH : cls.parser_author,
            INP_AUTH_MAIL   : cls.author_mail,
            INP_FOR_FILE    : cls.for_file,
            INP_FOR_REGION  : cls.for_region,
        }

    def __init__(self):
        self.check_items = {}
        self.split_point = IndexSign()

    def parse(self, data, **data_attrs):
        u"""
        override returns json
            {
                "data": [{...}, {...}, ...],
                "data_attrs": {...},
                "error": ...,
                "parser_info": {"parser_name": ...,
                                "parser_author": ...,
                                "parser_author_mail": ...,
                                "for_file_type": ...,
                                "for_region_type": ...}
            }
        and then takes parscope as wrapper
        """
        raise NotImplementedError

    def match(self, data, **data_attrs):
        raise NotImplementedError

class MainlandParser(_BaseParser):

    def parse(self, data, **data_attrs):
        raise NotImplementedError

    def match(self, data, **data_attrs):
        raise NotImplementedError

    def get_trade_account(self, data, **data_attrs):
        raise NotImplementedError

    def get_trade_date(self, data, **data_attrs):
        raise NotImplementedError

    def get_total_asset(self, data, **data_attrs):
        raise NotImplementedError

    def get_balance(self, data, **data_attrs):
        raise NotImplementedError

    def get_marketvalue(self, data, **data_attrs):
        raise NotImplementedError

    def get_netvalue(self, data, **data_attrs):
        raise NotImplementedError

    def get_financing(self, data, **data_attrs):
        raise NotImplemented

    def get_bonded_debt(self, data, **data_attrs):
        raise NotImplemented

    def get_bond_interest(self, data, **data_attrs):
        raise NotImplemented

    def get_total_liabilities(self, data, **data_attrs):
        raise NotImplemented

    def get_position(self, data, **data_attrs):
        raise NotImplementedError

    def get_trade_flow(self, data, **data_attrs):
        raise NotImplementedError

    def get_contract_flow(self, data, **data_attrs):
        raise NotImplemented

    def split_table(self, table, columns_kws, end_row_kws=None,
                    str_searchable=False, str_search_for='all',
                    starttriggerone=False, endtriggerone=False,
                    pullback=None):

        start_index = end_index = columns = None
        str_search_for_start = str_search_for_end = False
        str_search_for = str(str_search_for)

        if str_searchable is True:
            if str_search_for in ('all', '(0, 1)', '(1, 0)'):
                str_search_for_start = str_search_for_end = True
            elif str_search_for in ('0', 'start', '(0,)'):
                str_search_for_start = True
            elif str_search_for in ('1', 'end', '(1,)'):
                str_search_for_end = True

        end_row_kws = end_row_kws or [None]
        pullback = pullback or []

        for row_index, row_data in table.iterrows():
            #
            # 在一次完整的解析过程中
            # 当传入的table是一个完整的表时split_point才起效
            # 倘若传入的table为分割的表数据,split_point将变得毫无意义
            self.split_point.update_index(row_index + 1)

            row_items = row_data.tolist()
            row_str   = row_data.to_string(index=False)

            if start_index is None:
                #
                # 寻找表头位置
                if set(row_items) & set(columns_kws) == set(columns_kws):
                    columns = row_items
                    start_index = row_index + 1
                    continue
            else:
                if set(row_items) & set(end_row_kws) == set(end_row_kws):
                    #
                    # 寻找表尾位置
                    end_index = row_index - 1
                    break
                # if set(dataItems) == {numpy.nan}:  ## <- 个人经验：别使用这种方法
                elif not filter(lambda item: repr(item) != 'nan', row_items):
                    #
                    # 行数据全为nan即表尾
                    end_index = row_index - 1
                    break
                elif len(set(row_items) - {numpy.nan}) < 2 and not all(map(lambda _x: isinstance(_x, (int, float)), row_items)):
                    #
                    # 这里情况比较复杂,纯粹为了兼容所写
                    end_index = row_index - 1
                    break
                elif (start_index is not None) and (row_index == table.index[-1]):
                    #
                    # 最后一行数据
                    if all(map(lambda _key: _key in row_items, end_row_kws)):
                        end_index = row_index - 1
                    else:
                        end_index = row_index
                    break

            if (start_index is None) and (str_search_for_start is True):

                contains = [(column_kw in row_str) for column_kw in columns_kws]
                if all(contains) or ((starttriggerone is True) and any(contains)):
                    contain_all_start_row_kws = True
                else:
                    contain_all_start_row_kws = False
                if contain_all_start_row_kws is True:
                    columns = row_items
                    start_index = row_index + 1
                    continue

            if (end_index is None) and (str_search_for_end is True):

                contains = [end_row_kw in row_str for end_row_kw in end_row_kws]
                if all(contains) or ((endtriggerone is True) and any(contains)):
                    contain_all_end_row_key = True
                else:
                    contain_all_end_row_key = False
                if (start_index is not None) and (end_index is None) and (contain_all_end_row_key is True):
                    end_index = row_index - 1
                    break

            if (start_index is not None) and (end_index is not None):
                break

            for lw in pullback:
                if lw in row_str:
                    return

        if (start_index is not None) and (end_index is not None):
            mini_table = table.loc[start_index: end_index]
            mini_table.columns = columns
            return mini_table
        elif (start_index >= len(table)) and columns:
            mini_table = table.loc[start_index: start_index]
            mini_table.columns = columns
            return mini_table

    @staticmethod
    def adjust_columns(std_columns, actual_columns, dataframe, mapper=None):
        u"""
        用于调整解析提取过后的表列

        @std_columns        标准表头
        @actual_columns     实际处理的DataFrame表头
        @dataframe          待处理的DataFrame表数据
        @mapper             表头映射
        """
        #
        # 实际表头去除空格
        mapper = mapper or {}
        if getattr(actual_columns, 'fillna', None) is not None:
            actual_columns = actual_columns.fillna('__dirty')
        actual_columns = map(lambda _c: re.sub(u"\\s", "", _c) if isinstance(_c, str) else _c, actual_columns)

        #
        # 调整实际数据中符合标准列的数据
        new_columns = [mapper.get(col, col) for col in actual_columns]
        dataframe.columns = new_columns
        uselessCols = set(new_columns) - set(std_columns)
        dataframe.drop(columns=uselessCols, inplace=True, axis=1)

        #
        # 对于缺失的列进行补充
        lack_columns = set(std_columns) - set(dataframe.columns.tolist())
        for lack in lack_columns:
            dataframe[lack] = numpy.nan

        dataframe.dropna('index', 'all', inplace=True)
        dataframe.reset_index(drop=True, inplace=True)
        return dataframe

class CICCParser(_BaseParser):

    def parse(self, data, **data_attrs):
        raise NotImplementedError

    def match(self, data, **data_attrs):
        raise NotImplementedError

class UBSParser(_BaseParser):

    def parse(self, data, **data_attrs):
        raise NotImplementedError

    def match(self, data, **data_attrs):
        raise NotImplementedError

    def get_margin_summary(self, data, **data_attrs):
        raise NotImplementedError

    def get_trade_account(self, data, **data_attrs):
        raise NotImplementedError

    def get_trade_date(self, data, **data_attrs):
        raise NotImplementedError


BASE_CLASSES = (MainlandParser, CICCParser, UBSParser)


def floatreturn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        rt = func(*args, **kwargs)
        if rt is not None:
            if isinstance(rt, str):
                rt = rt.replace(',', '')
            try:
                rt = float(rt)
                if numpy.isnan(rt):
                    rt = None
            except (ValueError, UnicodeError):
                rt = None
        return rt
    return wrapper

def comfort_table(table, stdtype):
    std_columns  = set(stdtype.keys())
    lack_columns = std_columns - set(table.columns)
    for lack in lack_columns:
        table[lack] = numpy.nan
    df_table = table[list(std_columns)]
    df_table = df_table.astype(stdtype)
    return df_table


POSITION_COLUMNS_TYPES = OrderedDict(
    {
        u"证券代码" : str,  u"证券名称" : str,
        u"市价"     : float,    u"市值"     : float,
        u"盈亏"     : float,    u"股份余额" : float
    }
)

TRADE_FLOW_COLUMNS_TYPES = OrderedDict(
    {
        u"发生日期": str,   u"摘要"     : str,  u"证券代码" : str,  u"证券名称" : str,
        u"成交股数": float,     u"成交价格" : float,    u"发生金额" : float,    u"资金余额" : float,
        u"手续费"  : float,     u"印花税"   : float,    u"过户费"   : float,    u"清算费"   : float,
        u"佣金"    : float,     u"备注"     : str
    }
)

CONTRACT_FLOW_COLUMNS_TYPES = OrderedDict(
    {
        u"合约日期"       : str,  u"证券代码"       : str,  u"证券名称"   : str,  u"合约类型": str,
        u"未了结合约金额" : float,    u"未了结合约数量" : float,    u"未了结利息" : float,
        u"未了结费用"     : float,    u"待扣收"         : float,    u"归还截止日" : str
    }
)

TRADE_EVENTS = [u"证券买入", u"证券卖出", u"回购融券", u"股息入帐", u"红利入账", u"利息归本", u"股息红利扣税", u"红利差异税扣税",
                u"股息红利税补缴", u"股息个税征收", u"股份转出", u"托管转出", u"红股入账", u"证券调出", u"货币基金收益结转", u"融券购回",
                u"拆出质押购回", u"融券借入", u"拆出购回", u"偿还融券费用", u"前台收费", u"证券冻结", u'证券转银行', u"银行转取", u"申购配号",
                u"银行转证券", u"配股权证", u"融券回购到期预冻标券", u"权证上账", u"银证转入", u"资金长冻", u" 资产修正存", u"资产修正取",
                u"新股申购确认缴款", u"市值申购中签扣款回冲", u"交收资金冻结取消", u"新股中签资金扣款", u"市值申购中签扣款", u"交收资金冻结",
                u"市值申购中签", u"融券红利权益扣收", u"红利补偿金额扣收", u"还券划出", u"资金冻结取消", u"多还退券",
                u"现金蓝补", u"银证转出", u"新股入账", u"证券清理", u"转托管入", u"转托管出", u"融券转债权益扣收", u"指定交易", u"权证入帐",
                u"非流通证券转入", u"退出结算系统", u"申购中签\\(转非流通\\)", u"银行转存交行三方存管", u"银行转存", u"证券转入", u"托管转入",
                u"配股权证上账", u"配股缴款", u"回购拆出", u"配股缴款", u"回购拆出", u"红股派息", u"融券购回清算", u"买券还券", u"融券买券归还",
                u"非流通证券转出", u"上市流通", u"专项融券费用扣收", u"担保品买入", u"担保品卖出", u"债券质押回购融券清算", u"指定归还配股复权",
                u"融券证券划入", u"ETF申购扣费", u"ETF申购减股", u"ETF申购扣资", u"ETF申购", u"ETF赎回扣费", u"ETF赎回加股", u"ETF赎回返资",
                u"ETF赎回"]

# 账号数据所在位置标志(水平方向上)
HORIZON_TAGS = (u"信用资金帐号", u"信用资金帐号：", u"信用资金账号", u"信用资金账号：", u"信用客户号:",
                u"资产帐户：", u"资产账号:", u'资金帐号：',
                u"牛卡号:", u"牛卡号")
# 账号数据所在位置标志(垂直方向上)
VERTICAL_TAGS = (u"资产账户", u"资金帐号", u"客户号", u"资金账号",)