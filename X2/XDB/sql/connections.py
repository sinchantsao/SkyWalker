# coding=utf8
import logging
import pymysql
import sqlite3
import time
import typing as t
from os import environ, path
from threading import local, RLock
from X1.component import ComponentFeatureError
from X2.XDB.sql.table import BaseTable
_logger = logging.getLogger(__name__)

LocalConnections = local()
RemoteConnections = local()


class BaseSQLConnection(object):

    def connect(self):
        raise NotImplemented

    def execute(self, sql, value, fetchall=False, __insert_multi=False):
        raise NotImplemented

    def create(self, table: t.Type[BaseTable], wipe: bool = False) -> None:
        table(self.connect(), wipe).create()

    def drop(self, table: t.Type[BaseTable]) -> None:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f" DROP TABLE {table.TableName}; ")
        conn.commit()

    def insert_one(self, table: BaseTable, value: t.Tuple) -> None:
        """
        Args:
            table: 继承自 BaseTable 的类.
            value: 需要写入的数据, 按照 BaseTable.Columns 顺序给定.

        """
        sql = f"""
        INSERT INTO {table.TableName}({','.join([column for column in table.Columns])}) 
        VALUES ({','.join(["%s" for _ in range(len(table.Columns) + 1)])}); 
        """
        self.execute(sql, value, __insert_multi=False)

    def insert_multi(self, table: BaseTable, values: t.Iterable[t.Union[t.Tuple, t.List]]):
        sql = f"""
        INSERT INTO {table.TableName}({','.join([column for column in table.Columns])}) 
        VALUES ({','.join(["%s" for _ in range(len(table.Columns) + 1)])}); 
        """
        self.execute(sql, values, __insert_multi=True)

    def close(self):
        try:
            self.connect().close()
        except AttributeError:
            pass

class LocalStorage(BaseSQLConnection):
    DBName = "X2_SQLite_DB.db"
    __local__ = path.join(environ["HOME"], DBName)
    __lockers__ = {}

    def __init__(self,
                 dbpath: str,
                 max_retry: int = 100):
        super(LocalStorage, self).__init__()
        self.__local__ = dbpath
        # 一个线程一个连接, 一个数据库一个锁
        if self.__lockers__.get(self.__local__, None) is None:
            LocalStorage.__lockers__[self.__local__] = [RLock(), 1]
        else:
            LocalStorage.__lockers__[self.__local__][1] += 1

        self._max_retry = max_retry

    def connect(self) -> sqlite3.Connection:
        conn = getattr(LocalConnections, "__connection__", None)
        if conn is None:
            conn = sqlite3.connect(self.__local__)
            setattr(LocalConnections, "__connection__", conn)
            _logger.debug(f"Create SQLite connections connect with {self.__local__}")
        return conn

    def execute(self, sql, values, fetchall=False, onecol=False, __insert_multi=False) -> t.Union[t.List, None]:
        """
        执行 SQL 语句

        Args:
            sql: SQL 语句
            values: SQL 语句对应补缺参数.
            fetchall: 是否返回 SQL 执行结果数据.
            onecol: 是否只获取一列相关数据, 当为 True 时结果将会是一个列表且每个元素为单一元素而不是 Tuple.
            __insert_multi: 需要执行的是写入多行数据操作.

        Returns: List
        """

        retry = 0
        data = None
        # 线程锁避免当前应用线程抢占
        LocalStorage.__lockers__[self.__local__][0].acquire()
        try:
            conn = self.connect()
            if onecol:
                back_factory = conn.row_factory
                conn.row_factory = lambda cursor_, row: row[0]
            cursor = conn.cursor()
            while retry < self._max_retry:
                # 循环避免其他进程抢占导致访问操作失败
                # 失败重试上限 max_retry 自定义
                try:
                    if __insert_multi:
                        cursor.executemany(sql, values)
                    else:
                        cursor.execute(sql, values)
                except sqlite3.OperationalError as exc_err:
                    retry += 1
                    if retry >= self._max_retry:
                        raise ComponentFeatureError(
                            "SQLite busy ... helpless, try to adjust `max_retry` or avoid "
                            "SQLite being accessed by multi processes at the same time.\n"
                            f"SQL => {sql}\n"
                            f"VALUES => {values}"
                        )
                    time.sleep(0.1)
                    _logger.debug(f"Execute sql failed, retry again, {retry}.")
                    continue
                conn.commit()
                if fetchall:
                    data = cursor.fetchall()
                if onecol:
                    conn.row_factory = back_factory
                break
        finally:
            LocalStorage.__lockers__[self.__local__][0].release()
        return data

    def __del__(self):
        LocalStorage.__lockers__[self.__local__][1] -= 1
        if LocalStorage.__lockers__[self.__local__] == 0:
            del LocalStorage.__lockers__[self.__local__]

class MySQLStorage(BaseSQLConnection):

    def __init__(self, host: str = None, port: int = None, db: str = None, user: str = None, password: str = None):
        super(MySQLStorage, self).__init__()
        self._args = (host, port, db, user, password)

    def connect(self) -> pymysql.Connection:
        conn = getattr(RemoteConnections, "__connection__", None)
        if conn is None and self._args is not None:
            host, port, db, user, password = self._args
            conn = pymysql.Connection(host=host, port=int(port), db=db,
                                      user=user, password=password)
            setattr(RemoteConnections, "__connection__", conn)
            _logger.debug(f"Create MySQL connections connect on {user}@{host}:{port}/{db}")
        return conn

    def execute(self, sql: str, values: t.Tuple, fetchall: bool = False, __insert_multi: bool = False):
        conn = self.connect()
        cursor = conn.cursor()
        if __insert_multi:
            cursor.executemany(sql, values)
        else:
            cursor.execute(sql, values)
        conn.commit()

    def __del__(self):
        try:
            getattr(RemoteConnections, "__connection__", None).close()
        except (AttributeError, pymysql.err.Error):
            pass


