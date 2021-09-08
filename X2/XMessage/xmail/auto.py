# coding=utf8
import logging
import os
import sys
import threading
import time
import traceback
import typing as t
import warnings
from imaplib import IMAP4
from queue import Queue as ThreadQueue, Empty as EmptyQueueError
from X1.component import ComponentFeatureError
from X1.support import SysSupport
from X1.run import UnexpectedCompatible, RetryException
from X2.XMessage.xmail.connect import IMAPBox
from X2.XMessage.xmail.record import get_done_uids
from X2.XMessage.xmail.utils import uid_rules, restart_connection
from X2.XMessage.xmail.container import _MailData, MailEntity, MailContext, Attachment
from X2.XMessage.xmail.record import RecordsStorage
_logger = logging.getLogger(__name__)


UidQueue = ThreadQueue(maxsize=30)


class ProduceUID(threading.Thread):

    def __init__(self, imap_box: IMAPBox,
                 boxes: t.Iterable = None,
                 lookup_interval: int = 60 * 2):
        """
        Args:
            imap_box: X2.XMessage.xmail.connect.IMAPBox 对象
            boxes: 想要下载的邮箱文件夹, 默认为('INBOX'[收件箱], 'Junk'[垃圾箱])
            lookup_interval: UID 检索时间间隔,默认为 (60*2) 秒
        """
        super(ProduceUID, self).__init__()
        self.imap_box = imap_box
        self.lookup_interval = lookup_interval
        if boxes is None:
            self.boxes = ('INBOX', 'Junk')
            _logger.debug(f"Folders is not set, default folders {self.boxes} be set.")
        else:
            self.boxes = boxes
        self.todo_uids_map = {}

        # if local_uid_pointer is not None:
        #     self.local_uid_pointer = local_uid_pointer
        # else:
        #     self.local_uid_pointer = lambda f: (f, 1)

    def query_boxes_uid(self, boxes: t.Iterable = None, rules: t.Dict = None):
        """
        查询邮箱文件夹中的所有 UID,存储至 dict 返回.
        若未提供任何参数,根据实例化对象使用的参数进行获取.

        Args:
            boxes: 需要获取 UID 的邮箱文件夹名称序列,优先级别弱于 rules 参数
            rules: 获取邮箱文件夹中 UID 的限制规则{"文件夹名称": ["开始UID": "截至UID"]},优先根据该参数进行获取UID

        Returns: 文邮箱件夹名称为 key, UID 有序序列为 value 的 dict 数据

        """
        fu = {}
        if rules is not None:
            for box, limit in rules.items():
                fu[box] = self._query_box_uid_sbs(box, start=limit[0], end=limit[1])
            return fu

        if boxes is None:
            boxes = self.boxes
        for box in boxes:
            fu[box] = self._query_box_uid_sbs(box)
        return fu

    def _query_box_uid_sbs(self, box: str, start: int = 1, end: t.Union[str, int] = '*', segment: int = 100000):
        """
        由于邮箱协议限制,为了避免长文本 DDOS 攻击, 返回文本不得超过 100000 bytes,
        故需要进行分段进行获取 UID

        Args:
            box(str): 需要获取 UID 的文件夹.
            start(Optional[str, int]): 起始 UID 值.
            end(Optional[str, int]): 结束 UID 值, `*` 代表至最后一个 UID.
            segment(int): 默认为 10w, 根据测试 100000 bytes 实际限制大致在 15w~17w 之间,一般无需设置.

        Returns(list):  指定文件夹中的UID有序列表

        """
        start, end = uid_rules(start, end)
        uid_list = list()

        def enduid(limit, next_):
            return limit if next_ > limit else next_

        if end == '*':
            limit_max_uid = float('inf')
        else:
            limit_max_uid = end
        next_uid = start + segment
        end = enduid(limit_max_uid, next_uid)
        _logger.info(f"Wanna query UID from folder {box} by index from {start} to {limit_max_uid}.")
        while True:
            uid = self.imap_box.get_uid(box, start, end)
            if uid:
                uid_list.extend(uid)
                start = end + 1
                next_uid = start + segment
                end = enduid(limit_max_uid, next_uid)
                if end >= limit_max_uid:
                    break
            else:
                break
        if uid_list:
            uid_list = list(set(uid_list))
            _logger.info(f"Actually get mail uid info from {uid_list[0]} to {uid_list[-1]} from {box}, total {len(uid_list)}")
        return uid_list

    def _count_todo_uids(self):
        self.todo_uids_map.clear()
        for box in self.boxes:
            # local uids
            local_uids = get_done_uids(self.imap_box.username.split('@', 1)[0], box=box)
            # online uids
            online_uids = self._query_box_uid_sbs(box)
            todo_uids = set(online_uids) - set(local_uids)
            todo_uids = sorted(todo_uids)

            _logger.info(f"Folder => {box}: "
                         f"Local number of UID is {len(local_uids)}; "
                         f"Online number of UID is {len(online_uids)}; "
                         f"Diff number of UID is {len(todo_uids)}")

            self.todo_uids_map[box] = todo_uids

    def _pop_todo_uids(self):
        if not self.todo_uids_map:
            return
        for box, uids in self.todo_uids_map.items():
            for uid in uids:
                UidQueue.put((box, uid))
                _logger.debug(f"Put folder {box} UID {uid} into UID queue.")

    def run(self):
        last_looptime = time.time()

        while True:

            _logger.debug("PopUid thread start a new loop to get new mail uid info.")
            try:
                self._count_todo_uids()
            except BaseException as exc:
                _logger.warning("Something wrong with server, connection probably. reconnect later.\n[Detail] " + str(exc))
                restart_connection(self.imap_box, 60)
                continue
            self._pop_todo_uids()

            check_time = time.time()
            interval = check_time - last_looptime
            last_looptime = check_time
            if interval < self.lookup_interval:
                sleep_time = self.lookup_interval - interval
                time.sleep(sleep_time)
                _logger.debug(f"PopUid thread is sleeping, wake up after {sleep_time} seconds")
            _logger.debug(f"Now two minus has passed since last loop time")


class UIDDownloader(threading.Thread):

    X2_MAIL_DOWN_MYSQL_USER = os.environ.get("X2_MAIL_MYSQL_USER", None)
    X2_MAIL_DOWN_MYSQL_PASSWORD = os.environ.get("X2_MAIL_MYSQL_PASSWORD", None)
    X2_MAIL_DOWN_MYSQL_DB = os.environ.get("X2_MAIL_MYSQL_DB", None)
    X2_MAIL_DOWN_MYSQL_HOST = os.environ.get("X2_MAIL_MYSQL_HOST", None)
    X2_MAIL_DOWN_MYSQL_PORT = os.environ.get("X2_MAIL_MYSQL_PORT", None)

    def __init__(self, imap_box: IMAPBox,
                 sqlite_db: str = None,
                 mysql_db: tuple = None,
                 save_to_ceph: bool = False,
                 save_to_local: bool = False,
                 save_to_avenger: bool = False,
                 trigger: t.Union[
                     t.Iterable[t.Callable[[_MailData], None]],
                     t.Callable[[_MailData], None]
                 ] = None,
                 bucket: str = None,
                 local: str = None,
                 source: str = None,
                 retry_interval: int = 120):
        """
        下载线程

        Args:
            imap_box: 邮箱连接对象 X2.XMessage.xmail.connect.IMAPBox, 请确保一个线程单独一个连接不要多线程共享.
            sqlite_db: 需要存储到的本地 SQLite 数据库位置, 默认采用 $HOME/.mail_metadata.db .
            mysql_db: MySQL 连接元组参数 (host, port, db, user, password), 若未给定该参数则不能进行 MySQL 记录.
            save_to_ceph: 是否保存到 ceph 分布式存储, 如果希望为 True 需要设定相应环境变量,
                          相关环境变量参考相关环境变量请参考 X2.XMessage.xceph.get_default_boto3sev .
            save_to_local: 是否保存到本地.
            save_to_avenger: 是否保存到 Avenger 数据库.
            trigger: 每次下载存储到各自存储器后所触发的(一系列)操作, 其一必须接受参数为继承 _MailData 的类实例对象,
                     请参考 X2.XMessage.xmail.container .
            bucket: 当 save_to_ceph 为 True时, 必须设定 ceph 存储位置.
            local: 当 save_to_local 为 True时, 必须设定本地存储位置.
            source: 当 save_to_avenger 为 True时, 必须设定 Avenger 存储位置.

        """
        super(UIDDownloader, self).__init__()
        assert any((save_to_ceph, save_to_local, save_to_avenger))
        assert bool(save_to_ceph) == bool(bucket)
        assert bool(save_to_local) == bool(local)
        assert bool(save_to_avenger) == bool(source)

        self.imap_box = imap_box
        self.save_to_ceph = save_to_ceph
        self.save_to_local = save_to_local
        self.save_to_avenger = save_to_avenger
        if isinstance(trigger, t.Iterable):
            self.trigger = [self._default_trigger] + list(trigger)
        else:
            self.trigger = [self._default_trigger]
        self.bucket = bucket
        self.local = local
        self.source = source
        self.retry_interval = retry_interval
        self.recorder = RecordsStorage(
            sqlite_path=sqlite_db,
            mysql_db=(
                self.X2_MAIL_DOWN_MYSQL_HOST,
                self.X2_MAIL_DOWN_MYSQL_PORT,
                self.X2_MAIL_DOWN_MYSQL_DB,
                self.X2_MAIL_DOWN_MYSQL_USER,
                self.X2_MAIL_DOWN_MYSQL_PASSWORD
            )if mysql_db is None else mysql_db
        )

    def _default_trigger(self, mail_data, *args, **kwargs):
        if isinstance(mail_data, MailEntity):
            self.recorder.insert_mail_summary(mail_data, *args, **kwargs)
        elif isinstance(mail_data, MailContext):
            self.recorder.insert_mail_file_info(mail_data, *args, **kwargs)
        elif isinstance(mail_data, Attachment):
            self.recorder.insert_mail_file_info(mail_data, *args, **kwargs)

    def _request(self, box, uid):
        _logger.debug(f"Download mail by folder {box} & UID {uid}")
        try:
            mail = self.imap_box.get_mail_by_uid(box, uid)
        except (IMAP4.abort, ConnectionResetError) as conn_err:
            exc = str(conn_err)
            # 网络数据传输错误
            if "socket error: EOF" in exc:
                err_main = "Network transport error"
            # 网络请求错误
            elif "[Errno 104] Connection reset by peer" in str(conn_err):
                err_main = "Mail request frequently much"
            # server端错误
            elif "unexpected tagged response" in exc:
                err_main = "Unexpected mail response"
            else:
                error_msg = "Connection was broken with excepted error: \n" + (exc or "unknown")
                raise UnexpectedCompatible(error_msg)
            _logger.warning(f"{err_main}, request exception.")
            raise RetryException
        except Exception as exc:
            raise UnexpectedCompatible(str(exc)) from exc
        return mail

    def _run(self, box, uid):
        max_retry = 5
        retry_times = 0
        while True:
            try:
                mail = self._request(box, uid)
                break
            except RetryException:
                if retry_times < max_retry:
                    retry_times += 1
                    _logger.info(f"Restart connection and request [{box} - {uid}] again after {self.retry_interval} seconds. retry times: {retry_times}")
                    restart_connection(self.imap_box, sleeptime=self.retry_interval)
                    continue
                else:
                    _logger.error(f"Stop request {box} - {uid}, because request retry much.")
                    self.recorder.write_error_download(self.imap_box.username, box, uid, "retry much.")
                    # raise UnexpectedCompatible
                    # continue
                    return
            except UnexpectedCompatible as unexp:
                err_info = str(unexp)
                self.recorder.write_error_download(self.imap_box.username, box, uid, err_info)
                _logger.error(err_info)
                return

        # catch 主要是针对使用数据库错误
        try:
            if self.save_to_ceph:
                mail.write_to_ceph(bucket=self.bucket, prefix=mail.attr.user, trigger=self.trigger)
            if self.save_to_local:
                mail.write_to_unix(directory=self.local, trigger=self.trigger)
            if self.save_to_avenger:
                warnings.warn("Avenger Is Not Useful With Insert/Storage In Python3.x, Please Contact With The Avenger Department And Dev It.")
                mail.write_to_avenger(source=self.source, trigger=self.trigger)
            _logger.debug(f"Download done of folder {box} & UID {uid}")
        except (ComponentFeatureError, SysSupport) as exc:
            self.recorder.write_error_download(self.imap_box.username, box, uid, "Storage error.")
            _logger.error(f"{self.name} exist with exception code {exc.code}")

    def run(self):
        while True:
            try:
                box, uid = UidQueue.get()
                _logger.debug(f"Get folder {box} UID {uid} from UID queue.")
            except EmptyQueueError:
                _logger.error(traceback.format_exc())
                break

            self._run(box, uid)


