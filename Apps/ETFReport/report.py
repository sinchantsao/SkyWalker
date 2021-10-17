# coding=utf8

import pandas
import typing as t
from collections import OrderedDict

import os
import sys
CurrentWorkDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(CurrentWorkDir)))
from X2.utlis import SettingTree
from X2.XDB.avenger import get_default_client
from X4.date.china import get_next_trade_date

SettingTree.set_global_by_yaml(
    os.path.join(CurrentWorkDir, "ETFAccountInfo.yaml"),
    "AccountInfo"
)

data_cli = get_default_client()
source_name = "IT-WizardQuant-Information-P-ETFArbitrageTest"
PremarketTag = "AM"  # 盘后数据
AftermarketTag = "PM"  # 盘后数据


def set_pandas_display_options() -> None:
    # Ref: https://stackoverflow.com/a/52432757/
    display = pandas.options.display
    display.max_columns = 1000
    display.max_rows = 1000
    display.max_colwidth = 500
    display.width = 1000
    # display.precision = 2  # set as needed

set_pandas_display_options()

class DataField:
    Cap = "本金"
    PosValue = "持仓市值"
    Available = "可用资金"
    DepAndDraw = "出入金"
    UnreturnedAsset = "未返资金"
    EstPremarketAsset = "预估盘前资金"
    ActPremarketAsset = "实际盘前资金"
    EstAftermarketAsset = "预估盘后资金"
    ActAftermarketAsset = "实际盘后资金"
    BookNetAsset = "账面总资产净值"
    EstNetAsset = "预估总资产净值"
    ActNetAsset = "实际总资产净值"
    EstPNL = "预估总损益"
    ActPNL = "实际总损益"
    EstPNLRate = "预估总收益率"
    ActPNLRate = "实际总收益率"
    EstDailyPNL = "预估日损益金额"
    ActDailyPNL = "实际日损益金额"
    EstDailyPNLRate = "预估日收益率"
    ActDailyPNLRate = "实际日收益率"


def get_trade_dates(account: str,
                    start_trade_date: str = None,
                    end_trade_date: str = None) -> pandas.Series:
    """
    存入 avenger 哪些日期盘后结算数据就代表哪些日期进行了交易, 根据存入的结算数据查询交易日期

    Args:
        account: 交易账户
        start_trade_date: 截断查询开始日期 %Y%m%d
        end_trade_date: 截断交易日期 %Y%m%d

    Returns: pandas.Series[date[str]]
    """
    data_type = "Settlement"
    data_record: pandas.DataFrame = data_cli.queryDataFromSource(
        dataType='meta',
        source=source_name,
        type=data_type,
        isPandas=True,
        account=account,
        tag='PM',  # 盘后数据
    )
    trade_dates = data_record["date"]
    if start_trade_date is not None:
        trade_dates = trade_dates[trade_dates >= start_trade_date]
    if end_trade_date is not None:
        trade_dates = trade_dates[trade_dates <= start_trade_date]
    return trade_dates.sort_values() \
                      .reset_index(drop=True)


def get_market_data(account: str, trade_dates: t.Iterable) -> t.OrderedDict[str, t.Dict[str, pandas.DataFrame]]:
    """
    根据给定交易日期查询对应交易日盘前盘后资金数据.
    有盘后数据必须有盘前数据， 所以是成对的, 倘若缺一请与数据方联系.

    Args:
        account: 交易账户
        trade_dates: 交易日期

    Returns: t.OrderedDict[str, t.Dict[str, pandas.DataFrame]]
    """

    data_type = "Settlement"
    market_data = OrderedDict()
    for trade_date in trade_dates:
        aftermarket = data_cli.queryDataFromSource(
            dataType="raw",
            source=source_name,
            type=data_type,
            account=account,
            date=trade_date,
            tag=AftermarketTag,
        )[0]
        premarket = data_cli.queryDataFromSource(
            dataType="raw",
            source=source_name,
            type=data_type,
            account=account,
            date=trade_date,
            tag=PremarketTag,
        )[0]
        market_data[trade_date] = {PremarketTag: premarket,
                                   AftermarketTag: aftermarket}
    return market_data


def assemble_market_data(market_data: t.OrderedDict[str, t.Dict[str, pandas.DataFrame]],
                         init_asset: t.Union[int, float],
                         deposit_and_withdraw: t.Dict[str, t.Union[int, float]]):
    """
    Args:
        market_data: 盘前盘后资金数据
        init_asset: 账户初期本金
        deposit_and_withdraw: 账户资金存取变化情况
    """
    bnv = OrderedDict()     # Book Net Value   -> 账面总资产净值(持仓+余额)
    enav = OrderedDict()    # Estimated Net Asset Value  -> 预估总资产净值
    anav = OrderedDict()    # Actual Net Asset Value  -> 实际总资产净值
    caps = OrderedDict()    # CAP   -> 投入本金
    atpnl = OrderedDict()   # Actual Total Profit and Loss -> 实际总损益
    etpnl = OrderedDict()   # Estimated Total Profit and Loss -> 预估总损益
    epma = OrderedDict()    # Estimated Premarket Asset -> 预估盘前资金
    apma = OrderedDict()    # Actual Premarket Asset    -> 实际盘前资金
    eafta = enav            # Estimated Aftermarket Total Asset -> 预估盘后资金
    aafta = anav            # Actual Aftermarket Total Asset    -> 实际盘后资金
    avail = OrderedDict()   # Available     -> 资金余额/剩余现金
    pv = OrderedDict()      # PositionValue -> 持仓市值
    unrt = OrderedDict()    # Unreturned Asset  -> 未返还资

    capital = init_asset

    for trade_date, market_data_ in market_data.items():
        premarket_details = market_data_[PremarketTag]
        aftermarket_details = market_data_[AftermarketTag]

        if premarket_details.empty or aftermarket_details.empty:
            continue
        # ----------------------------------------------------------------------------------
        # 盘前数据
        # ----------------------------------------------------------------------------------
        # 预估盘前资金, 通过盘前数据最后一条数据中的 totalAsset 来作为预估盘前资金.
        # 但是还需要加上当日的出入金, 盘前数据没有体现出入金.
        #   - 理论上出入金都是发生在盘中，盘前数据本质上就是昨日的收盘收据.
        #     但如果出现了出入金发生在昨日收盘后，今日开盘前, 即:盘前数据
        #     totalAsset 已经算上了出入金, 那这里逻辑都要改了. 其实会非
        #     常麻烦，建议是和数据方沟通， 把盘前数据调整一下.

        # 当日出入金情况
        fund_change = deposit_and_withdraw.get(trade_date, 0)
        # 预估盘前资金
        epma[trade_date] = premarket_details.iloc[-1]["totalAsset"] + fund_change

        # 盘前数据分析提取
        for _, fund_state in premarket_details.iterrows():
            state_date = str(fund_state["tradeDate"])
            return0 = fund_state["unreturnAsset"] == 0

            # 当未返还资金为0时, 代表返还资金返还完毕, 此时的账户总资产资金情况为该条记录对应交易日收盘的实际资金情况.
            # 这里将作为后一交易日的实际盘前资金, 同样, 需要加上后一个交易日的出入金
            if return0:
                next_td = get_next_trade_date(state_date)
                dep_and_dra = deposit_and_withdraw.get(next_td, 0)
                # 实际盘前资金
                apma[next_td] = fund_state["totalAsset"] + dep_and_dra

        # ----------------------------------------------------------------------------------
        # 盘后数据
        # ----------------------------------------------------------------------------------
        # 当日账户最新状态 => 盘后数据最后一条
        cur_state = aftermarket_details.iloc[-1]

        # 本金处理 -> 初始本金 + 出入金变化
        capital_float = sum([deposit_and_withdraw[d] for d in deposit_and_withdraw if trade_date == d])
        capital += capital_float

        # 出金大于本金时, 本金清零, 从收益中继续扣除
        # 本来逻辑上本金扣完是需要继续扣除收益的,
        # 但是碍于收益情况由数据源间接提供(总资产-本金),数据源中就已经体现了出入金变化
        if capital <= 0:
            over_cost = capital
            capital = 0
        else:
            over_cost = 0
        caps[trade_date] = capital
        # 账面总资产净值 = 持仓 + 余额
        bnv[trade_date] = cur_state[["holdPosAsset", "cashAsset"]].sum()
        # 资金余额/剩余现金
        avail[trade_date] = cur_state["cashAsset"]
        # 持仓市值
        pv[trade_date] = cur_state["holdPosAsset"]
        # 预估总资产净值(直接从数据源中取数据)
        enav[trade_date] = cur_state["totalAsset"]
        # 未返还资金
        unrt[trade_date] = cur_state["unreturnAsset"]
        # 预估总损益 = 预估总资产净值 - 本金处理
        etpnl[trade_date] = enav[trade_date] = caps[trade_date]

        # 从当日的账户修正后的资金数据情况,查看历史返回资金情况,从中找到实际资金情况
        for _, fund_state in aftermarket_details.iterrows():
            # 当未返还资金为0时, 代表返还资金返还完毕, 此时的账户预估资产净值则为实际资产净值
            state_date = str(fund_state["tradeDate"])
            return0 = fund_state["unreturnAsset"] == 0
            # 写这个日期判断是因为为了限制某些没有的数据, 比如用户自定义处理账户从 20200101 开始的数据
            # 但某日详细数据中出现了 20200101 之前的数据, 找不到相应的数据就会出错/报错
            # 好像没有很好的解释清楚……anyway, 别动这个, 不然注释这个条件debug试试看也行
            is_legal_trade_date = state_date in market_data.keys()
            if return0 and is_legal_trade_date:
                anav[trade_date] = fund_state["totalAsset"]
                atpnl[trade_date] = anav[trade_date] - caps[trade_date]

    data_panel = pandas.DataFrame(
        data={
            DataField.Cap: caps,
            DataField.BookNetAsset: bnv,
            DataField.Available: avail,
            DataField.PosValue: pv,
            DataField.UnreturnedAsset: unrt,
            DataField.EstNetAsset: enav,
            DataField.ActNetAsset: anav,
            DataField.EstPNL: etpnl,
            DataField.ActPNL: atpnl,
            DataField.EstPremarketAsset: epma,
            DataField.ActPremarketAsset: apma,
            DataField.EstAftermarketAsset: eafta,
            DataField.ActAftermarketAsset: aafta,
        },
        index=caps.keys(),
        columns=[
            DataField.Cap,
            DataField.BookNetAsset,
            DataField.Available,
            DataField.PosValue,
            DataField.UnreturnedAsset,
            DataField.EstNetAsset,
            DataField.ActNetAsset,
            DataField.EstPNL,
            DataField.ActPNL,
            DataField.EstPremarketAsset,
            DataField.ActPremarketAsset,
            DataField.EstAftermarketAsset,
            DataField.ActAftermarketAsset,
        ]
    )
    data_panel.index = pandas.to_datetime(arg=data_panel.index.tolist(), format="%Y%m%d")
    data_panel.sort_index(inplace=True)
    return data_panel


if __name__ == '__main__':
    import AccountInfo

    account = AccountInfo["18369850"]
    tds = get_trade_dates("18369850", account.start)
    market_data = get_market_data("18369850", tds)
    panel = assemble_market_data(market_data=market_data, init_asset=account.principle, deposit_and_withdraw=account.change)
    print(panel)

