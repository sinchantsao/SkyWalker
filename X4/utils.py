# coding=utf8

from re import sub as substring
from X1.stand import ParamStandError


def clean_stock_name(stock_name: str) -> str:
    try:
        return substring("\\s", '', stock_name)
    except TypeError:
        raise ParamStandError(
            "Stock name match incorrectly, "
            "stock name should be a string, "
            f"but passing a {type(stock_name)}."
        )


def _stock_code_check(stock_code: str):
    if not stock_code.isdigit():
        raise ParamStandError(f"Stock code should be a pure digit series, but {stock_code}.")


