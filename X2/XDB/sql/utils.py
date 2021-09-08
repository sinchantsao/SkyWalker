# coding=utf8
import typing as t


def faint_conditions_sql_join(sql: str, field: str, kws: t.Union[t.List, t.Tuple]) -> str:
    """
    模糊匹配条件添加
    Args:
        sql: sql 查询语句
        field: 模糊匹配查询的字段
        kws: 模糊参数

    Returns: sql 语句
    """
    if kws is None:
        return sql
    condition_form = " WHERE {field} LIKE '%{first_value}%' "
    add_condition_form = "AND {field} LIKE '%{value}%' "
    if "WHERE" not in sql:
        sql += condition_form.format(field=field, first_value=kws[0])
        kws = kws[1:]
    sql += "".join([add_condition_form.format(field=field, value=value)
                    for value in kws])
    return sql


def exact_condition_sql_join(sql: str, field: str, kws: t.Union[t.List, t.Tuple]) -> str:
    """
    精确 sql 条件语句添加
    Args:
        sql: sql 查询语句
        field: 查询字段
        kws: 查询相关参数

    Returns: sql 语句
    """
    condition_form = " WHERE {field} = {first_value} "
    add_condition_form = "AND {field} = {value} "
    if "WHERE" not in sql and kws is not None:
        sql += condition_form.format(field=field,
                                     first_value=kws[0] if isinstance(kws[0], (float, int))
                                                        else f"'{kws[0]}'")
        kws = kws[1:]
    sql += "".join([add_condition_form.format(field=field, value=value if isinstance(value, (float, int)) else f"'{value}'")
                    for value in kws])
    return sql




