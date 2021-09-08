# coding=utf8
import datetime
import typing as t
from X1.stand import ParamStandError
from X2.XMessage.xmail.container import MailTimeFormat
from AvengerPy import AvengerAccessor
from X2.XMessage.xmail.record import MailMetaTable
from X2.XDB.sql.connections import LocalStorage, MySQLStorage
from X2.XDB.sql.utils import faint_conditions_sql_join, exact_condition_sql_join

class BaseMailRule:
    """
    根据该类对象数据进行数据选取
    """
    def __init__(self,
                 users: t.Tuple[str] = None,
                 box: t.Tuple[str] = None,
                 uid: t.Tuple[int] = None,
                 senders: t.Tuple[str] = None,
                 recipients: t.Tuple[str] = None,
                 carboncopies: t.Tuple[str] = None,
                 subject_kws: t.Tuple[str] = None,
                 filename_kws: t.Tuple[str] = None,
                 content_kws: t.Tuple[str] = None,
                 mail_time_span: t.Tuple[str, str] = None):
        self.users = users
        self.box = box
        self.uid = uid
        self.senders = senders
        self.recipients = recipients
        self.carboncopies = carboncopies
        self.subject_kws = subject_kws
        self.filename_kws = filename_kws
        self.content_kws = content_kws
        # ================================
        # TODO: 支持文本内容查找
        # ================================
        if mail_time_span is not None:
            try:
                [self.convert_mail_string_time_to_datetime(time_str)
                 for time_str in mail_time_span]
            except ValueError:
                raise ParamStandError(f"Time string should be format according to: {MailTimeFormat}")
        self.mail_time_span = mail_time_span

    @staticmethod
    def convert_mail_string_time_to_datetime(mail_time_string) -> datetime.datetime:
        """
        Args:
            mail_time_string: "%Y-%m-%d %H:%M:%S"
        Returns: datetime.datetime
        """
        return datetime.datetime.strptime(mail_time_string, MailTimeFormat)


class MailFiles:

    @staticmethod
    def records_from_sql(rule: BaseMailRule, sql_conn: t.Union[LocalStorage, MySQLStorage]):
        # ================================
        # TODO: 支持文本内容查找
        # ================================
        base_sql = f"SELECT * FROM {MailMetaTable.TableName} "

        base_sql = faint_conditions_sql_join(sql=base_sql, field=MailMetaTable.ColumnSubject, kws=rule.subject_kws)
        base_sql = faint_conditions_sql_join(sql=base_sql, field=MailMetaTable.ColumnSender, kws=rule.senders)
        base_sql = faint_conditions_sql_join(sql=base_sql, field=MailMetaTable.ColumnRecipient, kws=rule.recipients)
        base_sql = faint_conditions_sql_join(sql=base_sql, field=MailMetaTable.ColumnCC, kws=rule.carboncopies)
        base_sql = faint_conditions_sql_join(sql=base_sql, field=MailMetaTable.ColumnUser, kws=rule.subject_kws)

        base_sql = exact_condition_sql_join(sql=base_sql, field=MailMetaTable.ColumnUser, kws=rule.users)
        base_sql = exact_condition_sql_join(sql=base_sql, field=MailMetaTable.ColumnUid, kws=rule.uid)
        base_sql = exact_condition_sql_join(sql=base_sql, field=MailMetaTable.ColumnBox, kws=rule.box)

        return sql_conn.execute(base_sql, (), fetchall=True)

    @staticmethod
    def records_from_avenger(rule: BaseMailRule, avenger_conn: AvengerAccessor):
        raise NotImplementedError

