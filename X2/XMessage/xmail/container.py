# coding=utf8

import datetime
import os
from sqlite3 import OperationalError
import typing as t
from hashlib import md5
from io import BytesIO
from pathlib import Path
from pprint import pformat
from X1.stand import ArgStandError
from X1.component import ComponentFeatureError
from X1.support import SysSupport
from X2.XMessage.xmail import logger
from X2.utlis import create_dir
from X2.XDB.xceph import get_default_boto3sev, join_ceph_location, format_prefix, ceph_upload
from X4.date import TimeStdFmt


class _MailBase(object):
    def __init__(self, account: str,
                 box: str,
                 uid: int,
                 subject: str,
                 sender: str,
                 recipients: str,
                 carboncopies: str,
                 sendtime: datetime.datetime,
                 recvtime: datetime.datetime):
        """
        邮件基础信息对象

        Args:
            account: 邮箱账户
            box: 邮件文件夹
            uid: 邮件相对文件夹uid
            subject: 邮件主题
            sender: 邮件发件人
            recipients: 邮件接收者
            carboncopies: 邮件抄送人
            sendtime: 邮件发件时间
            recvtime: 邮件收件时间
        """

        username, vendor = account.split('@', 1)
        self.user = username
        self.vendor = vendor
        self.box = box.replace(' ', '&nbsp')
        self.uid = int(uid)
        self.subject = subject
        self.sender = sender
        self.recipients = recipients
        self.carboncopies = carboncopies
        self.sendtime = sendtime
        self.recvtime = recvtime

    def to_dict(self) -> t.Dict:
        return {
            'vendor': self.vendor,
            'user': self.user,
            'box': self.box,
            'uid': self.uid,
            'subject': self.subject,
            'sender': self.sender,
            'receivers': self.recipients,
            'cc': self.carboncopies,
            'sendtime': self.sendtime.strftime(TimeStdFmt),
            'recvtime': self.recvtime.strftime(TimeStdFmt),
        }

    def __str__(self):
        return pformat(self.to_dict())


class _MailData(object):

    def __init__(self,
                 account: str,
                 box: str,
                 uid: t.Union[int, str],
                 subject: str,
                 sender: str,
                 recipients: str,
                 carboncopies: str,
                 sendtime: datetime.datetime,
                 recvtime: datetime.datetime, ):
        """
        Args:
            account: 邮箱账户
            box: 邮箱文件夹
            uid: 邮箱文件夹相对uid
            subject: 邮件主题
            sender: 邮件发送人
            recipients: 邮件接收者
            carboncopies: 邮件抄送人
            sendtime: 邮件发件时间
            recvtime: 邮件接收时间
        """
        self.attr = _MailBase(account, box, uid, subject,
                              sender, recipients, carboncopies,
                              sendtime, recvtime)

    def write_to_ceph(self, bucket: str,
                      prefix: str = '',
                      trigger: t.Union[t.Iterable[t.Iterable[t.Callable]], t.Callable] = None,
                      *args, **kwargs):
        """
        正文数据存储到 ceph 分布式存储中

        Args:
            bucket: 需要存储到的 bucket, 其中不能包含斜杠(/).
            prefix: 文件目录层级, 可以理解成 Unix 系统中的目录路径.
            trigger: 需要触发的(多个)可执行操作, 可执行操作接收参数包括但不限于如下:
                - _MailData (子类)对象(第一参数);
                - storage_type(可选参数: 存储数据库类型;
                - storage_point(可选参数: 数据库的具体存储位置信息;
            *args: 正文和附件存储对应触发器所需要的参数.
            **kwargs: 正文和附件存储对应触发器所需要的参数.
        """
        raise NotImplementedError

    def write_to_avenger(self,
                         source,
                         trigger: t.Union[t.Iterable[t.Callable], t.Callable] = None,
                         *args, **kwargs):
        raise NotImplementedError

    def write_to_unix(self, directory: str,
                      trigger: t.Union[t.Iterable[t.Callable], t.Callable] = None,
                      *args, **kwargs):
        """
        正文数据存储到本地文件系统

        Args:
            directory: 存储路径(相对/绝对)
            trigger: 需要触发的(多个)可执行操作, 可执行操作接收参数包括但不限于如下:
                - _MailData (子类)对象(第一参数
                - storage_type(可选参数
                - storage_point(可选参数
            *args: 执行触发器所需要的参数
            **kwargs: 执行触发器所需要的参数
        """
        raise NotImplementedError

    def __str__(self):
        return self.attr.__str__()

def _execute_trigger(
        trigger: t.Union[
            t.Iterable[t.Callable[[_MailData], None]],
            t.Callable[[_MailData], None]
        ],
        self: _MailData,
        *args,
        **kwargs):
    try:
        if isinstance(trigger, t.Iterable):
            for tri in trigger:
                tri(self, *args, **kwargs)
        elif callable(trigger):
            trigger(self, *args, **kwargs)
    except OperationalError as db_op_err:
        error_info = str(db_op_err)
        if "SQLite database is locked" in error_info:
            logger.error("SQLite database is locked.")
        else:
            logger.error(f"Something wrong with SQLite database because {error_info}")
        raise ComponentFeatureError("Component of sqlite broken, please checkout log info.")


class MailFile(object):
    def __init__(self, filename: t.Union[bytes, str], raw: bytes, size: int = None):
        """
        邮件附件文件对象

        Args:
            filename: 附件文件原名称
            raw: 附件数据
            size: 文件大小
        """

        if isinstance(filename, bytes):
            filename = filename.decode('utf-8')
        self.filename = filename
        self.raw = raw
        if size is None:
            size = len(raw)
        self.size = size

    @property
    def filetype(self):
        prefull, ext = os.path.splitext(self.filename)

        if ext:
            file_type = ext
        else:
            if prefull.startswith('.'):
                file_type = prefull
            else:
                file_type = '.unknown'
        return file_type

    extension = filetype


class MailContext(_MailData):
    def __init__(self, account: str,
                 box: str,
                 uid: t.Union[int, str],
                 subject: str,
                 sender: str,
                 recipients: str,
                 carboncopies: str,
                 sendtime: datetime.datetime,
                 recvtime: datetime.datetime,
                 context: t.List[t.AnyStr], ):
        """
        邮件正文对象

        Args:
            context: 邮件正文文本
        """

        super(MailContext, self).__init__(
            account, box, uid, subject, sender, recipients, carboncopies, sendtime, recvtime)
        self.context = context
        self.fogname = f"{self.attr.user}_{self.attr.box}_{self.attr.uid}.context"

    def append(self, content):
        self.context.append(content)

    def write_to_unix(self, directory='', trigger=None, *args, **kwargs) -> None:
        """
        正文数据存储到本地文件系统

        Args:
            directory: 存储路径(相对/绝对)
            trigger: 需要触发的(多个)可执行操作, 可执行操作接收参数有但不限于如下:
                - _MailData (子类)对象(第一参数)
                - storage_type
                - storage_point
            *args: 执行触发器所需要的参数
            **kwargs: 执行触发器所需要的参数
        """

        kwargs.setdefault("storage_point", str(directory))
        directory = Path(directory).absolute()

        path = directory / self.fogname
        with open(str(path), "wb") as w:
            for line in self.context:
                w.write(line)
        logger.info(f"Write mail context '{self.fogname}' to inode '{str(directory)}'")

        _execute_trigger(trigger, self, *args, **kwargs)

    def write_to_ceph(self, bucket: str,
                      prefix: str = '',
                      trigger: t.Union[t.Iterable[callable], callable, None] = None,
                      *args, **kwargs):

        kwargs.setdefault("storage_point", join_ceph_location(bucket, prefix))

        ceph_conn = kwargs.get("ceph_conn", get_default_boto3sev())
        flow = BytesIO()
        for line in self.context:
            flow.write(line)
        response = ceph_upload(bytesflow=flow, bucket=bucket, prefix=prefix, fid=self.fogname, conn=ceph_conn)
        logger.info(f"Write mail context '{self.fogname}' to {bucket}[bucket] {prefix}[namespace]")
        logger.debug(response)

        _execute_trigger(trigger, self, *args, **kwargs)

    def write_to_avenger(self,
                         source,
                         trigger: t.Union[t.Iterable[callable], callable, None] = None,
                         *args, **kwargs):
        raise NotImplementedError

    def __str__(self):
        return '\n'.join(self.context)


class Attachment(_MailData):
    def __init__(self, account: str,
                 box: str,
                 uid: t.Union[int, str],
                 subject: str,
                 sender: str,
                 recipients: str,
                 carboncopies: str,
                 sendtime: datetime.datetime,
                 recvtime: datetime.datetime,
                 packfile: t.Union[MailFile, t.Tuple[t.Union[bytes, str], bytes, t.Union[int, None]]]):
        """
        邮件附件对象

        Args:
            packfile: 邮件附件附件对象/数据
        """
        super(Attachment, self).__init__(
            account, box, uid, subject, sender, recipients, carboncopies, sendtime, recvtime)

        if isinstance(packfile, tuple):
            packfile = MailFile(*packfile)
        if isinstance(packfile, MailFile):
            self.file = packfile
        else:
            raise ArgStandError("packfile should be a tuple or MailFile instance.")

        self.fogname = f"{self.attr.user}_" \
                       f"{self.attr.box}_" \
                       f"{self.attr.uid}_" \
                       f"{md5(self.file.filename.encode('utf8')).hexdigest()[:5]}" \
                       f"{self.file.filetype}"

    def __str__(self):
        return f"\n" \
               f"filename:{self.file.filename}\n" \
               f"fogname:{self.fogname}\n"

    def write_to_unix(self, directory='',
                      trigger: t.Union[t.Iterable[callable], callable, None] = None,
                      *args, **kwargs):

        kwargs.setdefault("storage_point", str(directory))

        directory = Path(directory).absolute()
        path = directory / self.fogname
        with open(str(path), "wb") as w:
            w.write(self.file.raw)
        logger.info(f"Write mail attachment '{self.fogname}' to '{str(directory)}'")

        _execute_trigger(trigger, self, *args, **kwargs)

    def write_to_ceph(self, bucket: str,
                      prefix: str = '',
                      trigger: t.Union[t.Iterable[callable], callable, None] = None,
                      *args, **kwargs):

        kwargs.setdefault("storage_point", join_ceph_location(bucket, prefix))

        ceph_conn = kwargs.get("ceph_conn", get_default_boto3sev())
        flow = BytesIO(self.file.raw)
        response = ceph_upload(bytesflow=flow, bucket=bucket, prefix=prefix, fid=self.fogname, conn=ceph_conn)
        logger.info(f"Write mail context '{self.fogname}' to {bucket}[bucket] {prefix}[namespace]")
        logger.debug(response)

        _execute_trigger(trigger, self, *args, **kwargs)

    def write_to_avenger(self,
                         source,
                         trigger: t.Union[t.Iterable[callable], callable, None] = None,
                         *args, **kwargs):
        # TODO
        raise NotImplemented


class Attachments(dict):
    def __init__(self, *args: Attachment):
        super(Attachments, self).__init__()
        for attach in args:
            self[attach.fogname] = attach


class MailEntity(_MailData):

    def __init__(self, context: MailContext,
                 attachments: Attachments,
                 **kwargs):
        """
        邮件对象, 封装了一封邮件所有相关数据

        Args:
            context: MailContext 邮件正文对象
            attachments: Attachments 所有附件字典封装对象
            **kwargs: 参考 _MailData
        """
        super(MailEntity, self).__init__(**kwargs)
        self.context = context
        self.attachments = attachments

    def write_to_ceph(self, bucket: str,
                      prefix: str = '',
                      trigger: t.Union[t.Iterable[callable], callable, None] = None,
                      *args, **kwargs):

        if '/' in bucket:
            raise ValueError("'/' is not allowed in bucket name")

        kwargs.setdefault("storage_type", "ceph")

        prefix = ''.join((format_prefix(prefix),
                          self.attr.sendtime.strftime('%Y%m%d'),
                          '/'))
        # 邮件基本信息记录触发
        _execute_trigger(trigger, self, *args, **kwargs)

        ceph_conn = kwargs.get("ceph_conn", get_default_boto3sev())
        kwargs.setdefault("ceph_conn", ceph_conn)
        # 正文存储
        self.context.write_to_ceph(bucket, prefix, trigger, *args, **kwargs)
        # 附件存储
        for attach in self.attachments.values():
            attach.write_to_ceph(bucket, prefix, trigger, *args, **kwargs)

    def write_to_unix(self, directory='',
                      trigger: t.Union[t.Iterable[callable], callable, None] = None,
                      *args, **kwargs):

        kwargs.setdefault("storage_type", "localhost")

        directory = Path(directory) / self.attr.sendtime.strftime('%Y%m%d')
        create_dir(str(directory))

        _execute_trigger(trigger, self, *args, **kwargs)

        self.context.write_to_unix(str(directory), trigger=trigger, *args, **kwargs)

        for attach in self.attachments.values():
            attach.write_to_unix(str(directory), trigger=trigger, *args, **kwargs)

    def write_to_avenger(self,
                         source,
                         trigger: t.Union[t.Iterable[t.Callable], t.Callable] = None,
                         *args, **kwargs):
        raise SysSupport("Avenger storage is not completed due to no writing hook for python3.x.")
