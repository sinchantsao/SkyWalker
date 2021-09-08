# coding=utf8
from X4.date import get_previous_trade_date,\
    get_trade_date_range,\
    get_next_trade_date, \
    get_future_trade_dates, \
    get_future_trade_date, \
    get_past_trade_dates, \
    get_past_trade_date

from X4.stock import get_code_market_belong, \
    get_code_industry_belong,\
    get_code_stock_name,\
    get_stock_name_code


if __name__ == '__main__':

    data = get_previous_trade_date('19901219')
    print(data)

    dates = get_trade_date_range("20210901", "20210914")
    print(dates)

    data = get_code_market_belong("000001")
    print(data)

    print(get_stock_name_code("协鑫集成"))
    print(get_stock_name_code("爱康科技"))

    data = get_code_industry_belong("000002")
    print(data)

    data = get_code_stock_name("000002")
    print(data)

    date = get_next_trade_date("20210903")
    print(date)

    dates = get_future_trade_dates("20210727", -5)
    print(dates)

    date = get_future_trade_date("20211225", 2)
    print(date)

    print(get_past_trade_date("20210905", 4))
    print(get_past_trade_dates("20210905", 4))
