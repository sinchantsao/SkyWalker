# coding=utf8

import pymysql
import sqlite3
import typing as t
from logging import getLogger
from X1.stand import IllegalOperationError
_logger = getLogger(__name__)


class _BaseTableNamespace(dict):
    # BaseTable Namespace
    def __init__(self):
        super(_BaseTableNamespace, self).__init__()
        self.columns = []

    def __setitem__(self, key, value):
        if key == "Columns":
            raise IllegalOperationError("`Columns` is a predefined argument, can not be set by user.")
        if key.startswith("Column") and value not in self.columns:
            self.columns.append(value)
        super(_BaseTableNamespace, self).__setitem__(key, value)

class _TableMeta(type):
    """
    对于 BaseTable 来说增加了 Columns 的整理.
    当继承 BaseTable 后, `Column` 开头的[自定义列]类属性将会被按照定义顺序整理到 Columns 类属性当中, Columns 作为被保护属性使用, 不被允许自定义.
    """
    @classmethod
    def __prepare__(metacls, name, bases):
        clsdict = _BaseTableNamespace()
        return clsdict

    def __new__(metacls, clsname, bases, classdict):
        result = type.__new__(metacls, clsname, bases, dict(classdict))
        result.Columns = classdict.columns
        return result

class BaseTable(metaclass=_TableMeta):
    TableName = ''
    InitSQL = ''

    def __init__(self, conn: t.Union[sqlite3.Connection, pymysql.Connection],
                 wipe: bool = False, formysql=False):
        """
        Args:
            conn: SQL连接
            wipe: 是否删除原有表
        """

        self.conn = conn
        self._wipe = wipe
        self._formysql = formysql

    def wipe(self) -> None:
        """ 删除表对象 """

        self.conn.cursor().execute(f"DROP TABLE IF EXISTS {self.TableName};")
        self.conn.commit()
        _logger.info(f"Delete table `{self.TableName}` if exists.")

    def create(self) -> None:
        """ 创建对象表 """

        if self._wipe:
            self.wipe()
        _logger.info(f"Create table `{self.TableName}` if not exists.")
        if self._formysql:
            mysql_default_args = ["DEFAULT CHARSET=utf8"]
            origin_args = self.InitSQL.split(';')
            full_args = origin_args[:-1] + mysql_default_args + origin_args[-1:]
            sql = " ".join(full_args)
        else:
            sql = self.InitSQL
        self.conn.cursor().execute(sql)
        self.conn.commit()

