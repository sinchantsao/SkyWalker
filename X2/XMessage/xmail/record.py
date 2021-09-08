# coding=utf8

import os
import rich
from threading import RLock
import typing as t
from enum import Enum
from X1.stand import ArgStandError
from X2.XDB.sql.connections import LocalStorage, MySQLStorage
from X2.XDB.sql.table import BaseTable
from X2.XDB.redison import get_redis_client
from X2.XMessage.xmail.container import MailEntity, MailContext, Attachment, MailTimeFormat


class MailMetaTable(BaseTable):
    """
    本表用于记录邮件主体的摘要信息
    """

    TableName = "mails_summary"

    ColumnUser = "user"
    ColumnBox = "box"
    ColumnUid = "uid"
    ColumnSubject = "subject"
    ColumnSender = "sender"
    ColumnRecipient = "recipients"
    ColumnCC = "cc"
    ColumnSendTime = "sendtime"
    ColumnRecvTime = "recvtime"

    InitSQL = f"""
    CREATE TABLE IF NOT EXISTS {TableName} (
      {ColumnUser}      VARCHAR(100) NOT NULL,  -- 邮箱账户名称(不包含域名/邮箱厂商)
      {ColumnBox}       VARCHAR(30) NOT NULL,   -- 邮箱文件夹
      {ColumnUid}       INT NOT NULL,           -- 邮件UID
      {ColumnSubject}   TEXT NOT NULL,          -- 邮件标题/主题
      {ColumnSender}    VARCHAR(100),           -- 邮件发送人
      {ColumnRecipient} TEXT NOT NULL,          -- 邮件收件人
      {ColumnCC}        TEXT,                   -- 邮件抄送人
      {ColumnSendTime}  DATETIME NOT NULL,      -- 邮件发送时间
      {ColumnRecvTime}  DATETIME NOT NULL,      -- 邮件接收时间
    PRIMARY KEY ({ColumnUser}, {ColumnBox}, {ColumnUid})
    );
    """


class MailFileTable(BaseTable):
    """
    本表用于记录邮件文件存储定位信息
    """

    TableName = "mails_files"

    ColumnUser = MailMetaTable.ColumnUser
    ColumnBox = MailMetaTable.ColumnBox
    ColumnUid = MailMetaTable.ColumnUid
    ColumnFogname = "fogname"
    ColumnOriginalName = "original_name"
    ColumnStorageType = "storage_type"
    ColumnStoragePoint = "storage_point"

    InitSQL = f"""
    CREATE TABLE IF NOT EXISTS {TableName} (
      {ColumnUser}          VARCHAR(100) NOT NULL,     -- 邮箱账户名称(不包含域名/邮箱厂商)
      {ColumnBox}           VARCHAR(30) NOT NULL,      -- 邮箱文件夹
      {ColumnUid}           INT NOT NULL,              -- 邮件UID
      {ColumnFogname}       VARCHAR(100),              -- 文件存储名称(为确保唯一性所生成的文件名: user_box_uid_md5.ext)
      {ColumnOriginalName}  TEXT,                      -- 文件原名称
      {ColumnStorageType}   VARCHAR(50) NOT NULL,      -- 存储形式名称/标记
      {ColumnStoragePoint}  VARCHAR(100) NOT NULL,     -- 存储位置定位
                                                         -- 1. 对于ceph(类s3存储)存储则为定位前缀
                                                         -- 2. 对于Avenger存储则为Source名称
                                                         -- 3. 对于服务器本地存储则为绝对路径文件夹
    PRIMARY KEY ({ColumnStorageType}, {ColumnStoragePoint}, {ColumnFogname}),
    FOREIGN KEY ({ColumnUser}, {ColumnBox}, {ColumnUid})
    REFERENCES {MailMetaTable.TableName}({ColumnUser}, {ColumnBox}, {ColumnUid})
    );
    """


class ErrorDownloadTable(BaseTable):
    """
    本表用于记录邮件下载错误记录
    """

    TableName = "error_downloads"

    ColumnUser = MailMetaTable.ColumnUser
    ColumnBox = MailMetaTable.ColumnBox
    ColumnUid = MailMetaTable.ColumnUid
    ColumnErrorMsg = "error_msg"

    InitSQL = f"""
    CREATE TABLE IF NOT EXISTS {TableName}(
      {ColumnUser}          VARCHAR(100) NOT NULL,     -- 邮箱账户名称(不包含域名/邮箱厂商)
      {ColumnBox}           VARCHAR(30) NOT NULL,      -- 邮箱文件夹
      {ColumnUid}           INT NOT NULL,              -- 邮件UID
      {ColumnErrorMsg}      TEXT,
    PRIMARY KEY ({ColumnUser}, {ColumnBox}, {ColumnUid})
    );
    """


# ======================================
# SQLite Thread Locker
# ======================================
_SQLiteLocker = RLock()
def _acquire_sqlite():
    _SQLiteLocker.acquire()
def _release_sqlite():
    _SQLiteLocker.release()


class RecordsStorage(object):
    default_sqlite = os.path.join(os.environ['HOME'], '.mail_metadata.db')

    # insert email summary info(actually replace instead).
    __InsertMailSummarySQL_mysql = f"""
    REPLACE INTO {MailMetaTable.TableName}(
      {MailMetaTable.ColumnUser},
      {MailMetaTable.ColumnBox},
      {MailMetaTable.ColumnUid},
      {MailMetaTable.ColumnSubject},
      {MailMetaTable.ColumnSender},
      {MailMetaTable.ColumnRecipient},
      {MailMetaTable.ColumnCC},
      {MailMetaTable.ColumnSendTime},
      {MailMetaTable.ColumnRecvTime}
    )
    VALUES (
      %({MailMetaTable.ColumnUser})s,
      %({MailMetaTable.ColumnBox})s,
      %({MailMetaTable.ColumnUid})s,
      %({MailMetaTable.ColumnSubject})s,
      %({MailMetaTable.ColumnSender})s,
      %({MailMetaTable.ColumnRecipient})s,
      %({MailMetaTable.ColumnCC})s,
      %({MailMetaTable.ColumnSendTime})s,
      %({MailMetaTable.ColumnRecvTime})s
    );
    """
    __InsertMailSummarySQL_sqlite = f"""
    REPLACE INTO {MailMetaTable.TableName}(
      {MailMetaTable.ColumnUser},
      {MailMetaTable.ColumnBox},
      {MailMetaTable.ColumnUid},
      {MailMetaTable.ColumnSubject},
      {MailMetaTable.ColumnSender},
      {MailMetaTable.ColumnRecipient},
      {MailMetaTable.ColumnCC},
      {MailMetaTable.ColumnSendTime},
      {MailMetaTable.ColumnRecvTime}
    )
    VALUES (
      :{MailMetaTable.ColumnUser},
      :{MailMetaTable.ColumnBox},
      :{MailMetaTable.ColumnUid},
      :{MailMetaTable.ColumnSubject},
      :{MailMetaTable.ColumnSender},
      :{MailMetaTable.ColumnRecipient},
      :{MailMetaTable.ColumnCC},
      :{MailMetaTable.ColumnSendTime},
      :{MailMetaTable.ColumnRecvTime}
    );
    """
    # insert mail attachment files base info(actually replace instead).
    __InsertMailFileInfoSQL_mysql = f"""
    REPLACE INTO {MailFileTable.TableName}(
      {MailFileTable.ColumnUser},
      {MailFileTable.ColumnBox},
      {MailFileTable.ColumnUid},
      {MailFileTable.ColumnFogname},
      {MailFileTable.ColumnOriginalName},
      {MailFileTable.ColumnStorageType},
      {MailFileTable.ColumnStoragePoint}
    )
    VALUES(
      %({MailFileTable.ColumnUser})s,
      %({MailFileTable.ColumnBox})s,
      %({MailFileTable.ColumnUid})s,
      %({MailFileTable.ColumnFogname})s,
      %({MailFileTable.ColumnOriginalName})s,
      %({MailFileTable.ColumnStorageType})s,
      %({MailFileTable.ColumnStoragePoint})s
    );
    """
    __InsertMailFileInfoSQL_sqlite = f"""
    REPLACE INTO {MailFileTable.TableName}(
      {MailFileTable.ColumnUser},
      {MailFileTable.ColumnBox},
      {MailFileTable.ColumnUid},
      {MailFileTable.ColumnFogname},
      {MailFileTable.ColumnOriginalName},
      {MailFileTable.ColumnStorageType},
      {MailFileTable.ColumnStoragePoint}
    )
    VALUES(
      :{MailFileTable.ColumnUser},
      :{MailFileTable.ColumnBox},
      :{MailFileTable.ColumnUid},
      :{MailFileTable.ColumnFogname},
      :{MailFileTable.ColumnOriginalName},
      :{MailFileTable.ColumnStorageType},
      :{MailFileTable.ColumnStoragePoint}
    );
    """
    # insert error info while downloading(actually replace instead).
    __InsertMailErrorSQL_mysql = f"""
    REPLACE INTO {ErrorDownloadTable.TableName}(
      {ErrorDownloadTable.ColumnUser},
      {ErrorDownloadTable.ColumnBox},
      {ErrorDownloadTable.ColumnUid},
      {ErrorDownloadTable.ColumnErrorMsg}
    )
    VALUES(
      %({ErrorDownloadTable.ColumnUser})s,
      %({ErrorDownloadTable.ColumnBox})s,
      %({ErrorDownloadTable.ColumnUid})s,
      %({ErrorDownloadTable.ColumnErrorMsg})s,
    );
    """
    __InsertMailErrorSQL_sqlite = f"""
    REPLACE INTO {ErrorDownloadTable.TableName}(
      {ErrorDownloadTable.ColumnUser},
      {ErrorDownloadTable.ColumnBox},
      {ErrorDownloadTable.ColumnUid},
      {ErrorDownloadTable.ColumnErrorMsg}
    )
    VALUES(
      :{ErrorDownloadTable.ColumnUser},
      :{ErrorDownloadTable.ColumnBox},
      :{ErrorDownloadTable.ColumnUid},
      :{ErrorDownloadTable.ColumnErrorMsg},
    );
    """

    def __init__(self, tables: t.Iterable[BaseTable] = None,
                 wipe: bool = False,
                 sqlite_path: str = None,
                 mysql_db: t.Tuple[t.Union[str, None],
                                   t.Union[int, None],
                                   t.Union[str, None],
                                   t.Union[str, None],
                                   t.Union[str, None]] = None):
        """
        用于存储邮箱下载数据记录存储

        默认情况下会在 $HOME 目录下创建一个 SQLite 数据库,
        当然也可以自定义该 SQLite 数据库位置 sqlite_path.

        SQLite 存储选项是不能取消的, 作用主要两点
          - 无 MySQL 服务只能本地存储.
          - 备份 MySQL 存储, 避免 MySQL 服务不可用.

        Args:
            tables: 基于 X2.XDB.sql.table.BaseTable 的表类, 一般情况下不给定参数, 使用默认参数.
                    即: 1. 邮件摘要信息表 MailMetaTables;
                        2. 邮件附件文件基本信息表 MailFileTable;
                        3. 下载错误信息记录表 ErrorDownloadTable;
            wipe: 是否删除原有的 SQL 表对象, 一般情况下不给顶参数使用默认参数, 同时该参数配合 tables 参数使用.
            sqlite_path: 自定义 SQLite 数据库位置, Default: $HOME/.mail_metadata.db .
            mysql_db: MySQL 连接元组参数 (host, port, db, user, password), 若未给定该参数则不能进行 MySQL 记录.
        """
        self._local_ = LocalStorage(dbpath=sqlite_path or RecordsStorage.default_sqlite)
        if mysql_db is not None and None not in mysql_db:
            self._remote_ = MySQLStorage(*mysql_db)
            self._remote_.connect()
        else:
            self._remote_ = None
        self._remote_: t.Union[MySQLStorage, None]

        if not isinstance(tables, t.Iterable):
            tables = (MailMetaTable, MailFileTable, ErrorDownloadTable)

        self.local_tables = {
            table.TableName: table(self._local_.connect(), wipe=wipe)
            for table in tables
        }
        self.remote_tables = {
            table.TableName: table(self._remote_.connect(), wipe=wipe, formysql=True)
            for table in tables
        } if self._remote_ is not None else {}

    def setup_sql_table(self) -> None:
        for table in self.local_tables.values():
            table.create()
        for table in self.remote_tables.values():
            table.create()

    def insert_mail_summary(self, entity: MailEntity,
                            *args, **kwargs) -> None:
        """
        写入邮件主体基本信息.

        数据录入采用 REPLACE 而不是 INSERT, 对于重复数据将会覆盖,
        主键为 user / box / uid 三个字段, 根据该三个字段数据进行写入.

        Args:
            entity: 邮件封装类 MailEntity 对象.

        """

        data = {
            MailMetaTable.ColumnUser: entity.attr.user,
            MailMetaTable.ColumnBox: entity.attr.box,
            MailMetaTable.ColumnUid: int(entity.attr.uid),
            MailMetaTable.ColumnSubject: entity.attr.subject,
            MailMetaTable.ColumnSender: entity.attr.sender,
            MailMetaTable.ColumnRecipient: entity.attr.recipients,
            MailMetaTable.ColumnCC: entity.attr.carboncopies,
            MailMetaTable.ColumnSendTime: entity.attr.sendtime.strftime(MailTimeFormat),
            MailMetaTable.ColumnRecvTime: entity.attr.recvtime.strftime(MailTimeFormat),
        }

        self._local_.execute(self.__InsertMailSummarySQL_sqlite, data)
        if self._remote_ is not None:
            self._remote_.execute(self.__InsertMailSummarySQL_mysql, data)

    def insert_mail_file_info(self,
                              file: t.Union[MailContext, Attachment],
                              storage_type: str,
                              storage_point: str,
                              *args, **kwargs) -> None:
        """
        写入邮件附件和正文文件信息.

        数据录入采用 REPLACE 而不是 INSERT, 对于重复数据将会覆盖,
        主键为 storage_type / storage_point / fogname 三个字段.

        Args:
            file: 邮件附件对象/邮件正文对象
            storage_type: 存储数据库类型
            storage_point: 存储位置
        """

        data = {
            MailFileTable.ColumnUser: file.attr.user,
            MailFileTable.ColumnBox: file.attr.box,
            MailFileTable.ColumnUid: file.attr.uid,
            MailFileTable.ColumnFogname: file.fogname,
            MailFileTable.ColumnOriginalName: file.file.filename if isinstance(file, Attachment) else "",
            MailFileTable.ColumnStorageType: storage_type,
            MailFileTable.ColumnStoragePoint: storage_point,
        }

        self._local_.execute(self.__InsertMailFileInfoSQL_sqlite, data)
        if self._remote_ is not None:
            self._remote_.execute(self.__InsertMailFileInfoSQL_mysql, data)

    def write_error_download(self, user: str, box: str, uid: int, error_msg: str = None):
        data = {
            ErrorDownloadTable.ColumnUser: user,
            ErrorDownloadTable.ColumnBox: box,
            ErrorDownloadTable.ColumnUid: uid,
            ErrorDownloadTable.ColumnErrorMsg: error_msg,
        }
        self._local_.execute(self.__InsertMailErrorSQL_sqlite, data)
        if self._remote_ is not None:
            self._remote_.execute(self.__InsertMailErrorSQL_mysql, data)

    @classmethod
    def publish_newfile_info(cls, file: t.Union[MailContext, Attachment],
                             *args, **kwargs):
        conn = get_redis_client()
        conn.publish_json_message(
            "email",
            {
                "user": file.attr.user,
                "folder": file.attr.box,
                "uid": file.attr.uid,
                "fogname": file.fogname
            }
        )

    def get_done_uids(self, box: t.AnyStr) -> t.List:
        """
        读取 UID 信息.
        由于 SQLite 必定(或者说必须)起作用, 将本地 SQLite 读取 UID 信息.

        Args:
            box: 邮箱文件夹名称

        Returns: UID列表

        """
        sql = f"""
        SELECT {MailMetaTable.ColumnUid}
        FROM {MailMetaTable.TableName}
        WHERE {MailMetaTable.ColumnBox} == ?;
        """
        result = self._local_.execute(sql, (box,), fetchall=True, onecol=True)
        return result


class SQLServerType(Enum):
    MySQL = 1
    SQLite = 2


def init_records(sync2point: SQLServerType, wipe=False,
                 mysql_location: t.Tuple[str, int, t.Union[str, None], str, t.Union[str, None]] = None,
                 sqlite_path: str = None) -> None:
    """
    初始化数据库, 建表/同步 SQL 存储之间的数据

    Args:
        sqlite_path:
        sync2point: 同步的基准是哪个数据库
        wipe: 是否删除原有表数据, 一般不使用该参数
        mysql_location: 当基准数据库为 SQLite 时, 被同步到数据库为 MySQL,
                    需要指定相应参数, 如果不同步也可以不入参
    """

    recorder = RecordsStorage(wipe=wipe, mysql_db=mysql_location, sqlite_path=sqlite_path)
    rich.print(f"[b yellow]SQLite: [i blue]{recorder.default_sqlite}")
    # 建表
    recorder.setup_sql_table()

    # 同步数据 确定同步方向
    if sync2point is SQLServerType.SQLite:
        resource_conn = recorder._local_.connect()
        target_conn = recorder._remote_ is not None and recorder._remote_.connect()
        target_endpoint = SQLServerType.MySQL
    elif sync2point is SQLServerType.MySQL:
        resource_conn = recorder._remote_ is not None and recorder._remote_.connect()
        target_conn = recorder._local_.connect()
        target_endpoint = SQLServerType.SQLite
    else:
        raise ArgStandError(f"sync2point should be {SQLServerType} instead of {type(sync2point)}")

    if not all((resource_conn, target_conn)):
        # 未传参或者某种情况导致连接失败
        rich.print("[bold red][Warning] Mail Records Synchronization Failed, Resource/Target SQL Server Missing.")
        return
    resource_endpoint = sync2point

    # literal = getattr(resource_conn, "literal", getattr(target_conn, "literal", None))
    resource_cursor = resource_conn.cursor()
    target_cursor = target_conn.cursor()

    # 查询`被同步到`数据库每个邮箱文件夹最高 UID.
    target_cursor.execute(
        f"SELECT {MailMetaTable.ColumnUser}, {MailMetaTable.ColumnBox}, MAX({MailMetaTable.ColumnUid}) "
        f"FROM {MailMetaTable.TableName} "
        f"GROUP BY {MailMetaTable.ColumnUser}, {MailMetaTable.ColumnBox};"
    )
    uid_info_groups = target_cursor.fetchall()
    # 从未同步过的情况/被同步到的数据库为新数据库.
    # 查看记录种有哪些邮箱账户+文件夹组合, 从 UID 为 0 开始同步.
    if not uid_info_groups:
        resource_cursor.execute(
            f"""
            SELECT {MailMetaTable.ColumnUser}, {MailMetaTable.ColumnBox}, 0 
            FROM {MailMetaTable.TableName} 
            GROUP BY {MailMetaTable.ColumnUser}, {MailMetaTable.ColumnBox};
            """
        )
        uid_info_groups = resource_cursor.fetchall()

    summary_cols_present = ','.join(MailMetaTable.Columns)
    summary_placeholders = ','.join(['%s' for i in range(len(MailMetaTable.Columns))])
    file_record_cols_present = ','.join(MailFileTable.Columns)
    file_record_placeholders = ','.join(['%s' for i in range(len(MailFileTable.Columns))])
    err_cols_present = ','.join(ErrorDownloadTable.Columns)
    err_placeholders = ','.join(['%s' for i in range(len(ErrorDownloadTable.Columns))])

    from rich.console import Console as ColorPrint
    color_print = ColorPrint()
    order_num = 0
    for order_num, (user, box, max_uid) in enumerate(uid_info_groups):
        # `被同步`数据库中需要同步的邮件主体信息数据.
        resource_cursor.execute(
            f"""
            SELECT {summary_cols_present} 
            FROM {MailMetaTable.TableName} 
            WHERE {MailMetaTable.ColumnUser} = '{user}' AND 
                  {MailMetaTable.ColumnBox} = '{box}' AND 
                  {MailMetaTable.ColumnUid} > {max_uid};
            """
        )
        syncing_summary_data: t.List[t.Tuple] = resource_cursor.fetchall()
        # 每一账户/每一文件夹 邮件主体信息数据.
        with color_print.status(f"[b cyan]Syncing Mail Summary Info\n"
                                f"[b cyan]From: [i blue]{resource_endpoint}\n"
                                f"[b cyan]To: [i blue]{target_endpoint}\n"
                                f"[b cyan]User: [i blue]{user}\n"
                                f"[b cyan]Box: [i blue]{box}"):
            for user_r, box_r, uid, subject, sender, recipients, cc, sendtime, recvtime in syncing_summary_data:
                # user, box, uid, subject, sender, recipients, cc, sendtime, recvtime = line
                # if literal is not None:
                #     subject = literal(subject)
                #     recipients = literal(recipients)
                #     cc = literal(cc)

                target_cursor.execute(
                    f"""
                    REPLACE INTO {MailMetaTable.TableName}({summary_cols_present})
                    VALUES({summary_placeholders});
                    """,
                    (user_r, box_r, uid, subject, sender, recipients, cc, sendtime, recvtime)
                )
                target_conn.commit()
        rich.print(f"[b yellow]{order_num})[i blue]Summary ({user} - {box})")

        # `被同步`数据库中需要同步的邮件附件文件记录数据.
        resource_cursor.execute(
            f"""
            SELECT {file_record_cols_present} 
            FROM {MailFileTable.TableName} 
            WHERE {MailFileTable.ColumnUser} = '{user}' AND 
                  {MailFileTable.ColumnBox} = '{box}' AND 
                  {MailFileTable.ColumnUid} > {max_uid};
            """
        )
        syncing_file_record_data: t.List[t.Tuple] = resource_cursor.fetchall()
        # 每一账户/每一文件夹 邮件附件文件记录数据
        with color_print.status(f"[b cyan]Syncing Mail File Records\n"
                                f"[b cyan]From: [i blue]{resource_endpoint}\n"
                                f"[b cyan]To: [i blue]{target_endpoint}\n"
                                f"[b cyan]User: [i blue]{user}\n"
                                f"[b cyan]Box: [i blue]{box}"):
            for user_r, box_r, uid, fogname, original_name, storage_type, storage_point in syncing_file_record_data:
                # user, box, uid, fogname, original_name, storage_type, storage_point = line
                target_cursor.execute(
                    f"""
                    REPLACE INTO {MailFileTable.TableName} 
                    VALUES ({file_record_placeholders});
                    """,
                    (user_r, box_r, uid, fogname, original_name, storage_type, storage_point)
                )
                target_conn.commit()
        rich.print(f"[b yellow]{order_num})[i blue]Files ({user} - {box})")

    # 异常下载记录(一般异常下载数量不多且会删除,所以一次性同步).
    resource_cursor.execute(
        f"""
        SELECT {err_cols_present} 
        FROM {ErrorDownloadTable.TableName};
        """
    )
    syncing_err_records_data = resource_cursor.fetchall()
    # 同步异常下载记录
    with color_print.status(f"[b cyan]Syncing Error Download Records"):
        for user_r, box_r, uid, error_msg, in syncing_err_records_data:
            target_cursor.execute(
                f"""
                REPLACE INTO {ErrorDownloadTable.TableName} 
                VALUES ({err_placeholders});
                """,
                (user_r, box_r, uid, error_msg, )
            )
            target_conn.commit()
    rich.print(f"[b yellow]{order_num+1})[i blue]Errors")
    rich.print("[b green]Complete!")


# notify trigger
def publish_mailfileinfo(instance: t.Union[Attachment, MailContext], *args, **kwargs):
    conn = get_redis_client()
    conn.publish_json_message("email", {"user": instance.attr.user,
                                        "folder": instance.attr.box,
                                        "uid": instance.attr.uid,
                                        "fogname": instance.fogname})


def get_done_uids(user: str, box: t.AnyStr) -> t.List:
    """
    读取 UID 信息.
    由于 SQLite 必定(或者说必须)起作用, 将本地 SQLite 读取 UID 信息.

    Args:
        user: 邮箱用户
        box: 邮箱文件夹名称

    Returns: UID列表

    """
    local_storage = LocalStorage(dbpath=RecordsStorage.default_sqlite)
    sql = f"""
    SELECT {MailMetaTable.ColumnUid}
    FROM {MailMetaTable.TableName}
    WHERE {MailMetaTable.ColumnUser} == ?
    AND {MailMetaTable.ColumnBox} == ?;
    """
    result = local_storage.execute(sql, (user, box, ), fetchall=True, onecol=True)
    return result
