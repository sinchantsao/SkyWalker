# coding=utf8

import smtplib
import typing as t
import ssl as pythonssllib
from imaplib import IMAP4, IMAP4_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from X2.XMessage.xmail.utils import _sort_attach

from X2.XMessage.xmail import logger
from X2.XMessage.xmail.container import MailEntity
from X2.XMessage.xmail.utils import split_uid, status_is_ok, response_is_ok
from X2.XMessage.xmail.parse import built_entity


class IMAPTransport:

    def __init__(self, hostname: str,
                 port: int = None,
                 ssl: bool = True,
                 ssl_context: pythonssllib.SSLContext = None,
                 starttls: bool = False):
        self.hostname = hostname
        self.ssl = ssl
        self.ssl_context = ssl_context
        self.starttls = starttls

        if self.ssl:
            self.port = port or 993
            if self.ssl_context is None:
                self.ssl_context = pythonssllib.create_default_context()
            self.server = IMAP4_SSL(self.hostname, self.port, ssl_context=self.ssl_context)
        else:
            self.port = port or 143
            self.server = IMAP4(self.hostname, self.port)

        if self.starttls:
            self.server.starttls()
        logger.info(f"Created IMAP4 transport for {self.hostname}:{self.port}")

    def connect(self, username: str, password: str):
        self.server.login(username, password)
        self.server.select()
        logger.info(f"Logged into server {self.hostname} and selected mailbox 'INBOX'")
        return self.server


class IMAPBox(object):

    def __init__(self, hostname: str,
                 port: int = None,
                 username: str = None,
                 password: str = None,
                 ssl: bool = True,
                 ssl_context: pythonssllib.SSLContext = None,
                 starttls: bool = False):

        self.server = IMAPTransport(hostname=hostname, port=port, ssl=ssl,
                                    ssl_context=ssl_context, starttls=starttls)

        self.username = username
        self.password = password

        self.connection = self.server.connect(username, password)

        logger.info(f"Connected to IMAP Server with user {username} on {hostname}{' over SSL' if ssl or starttls else ''}")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.logout()

    def reconnect(self):
        self.server = IMAPTransport(hostname=self.server.hostname, port=self.server.port, ssl=self.server.ssl,
                                    ssl_context=self.server.ssl_context, starttls=self.server.starttls)
        self.connection = self.server.connect(self.username, self.password)

    def logout(self):
        self.connection.close()
        self.connection.logout()
        logger.info(f"Disconnected from IMAP Server {self.server.hostname}@{self.username}")

    def mark_seen(self, uid: str):
        logger.info("Mark UID {} with \\Seen FLAG".format(int(uid)))
        self.connection.uid('STORE', uid, '+FLAGS', '(\\Seen)')

    def mark_flag(self, uid: str):
        logger.info("Mark UID {} with \\Flagged FLAG".format(int(uid)))
        self.connection.uid('STORE', uid, '+FLAGS', '(\\Flagged)')

    def delete(self, uid: str):
        logger.info(
            "Mark UID {} with \\Deleted FLAG and expunge.".format(int(uid)))
        self.connection.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
        self.connection.expunge()

    def copy(self, uid: str, destination_folder: str):
        logger.info("Copy UID {} to {} folder".format(
            int(uid), str(destination_folder)))
        return self.connection.uid('COPY', uid, destination_folder)

    def move(self, uid: str, destination_folder: str):
        logger.info("Move UID {} to {} folder".format(
            int(uid), str(destination_folder)))
        if self.copy(uid, destination_folder):
            self.delete(uid)

    def _change_workfolder(self, folder):
        status, content = self.connection.select(folder)
        if not status_is_ok(status):
            raise IMAP4.error(f"Failed to select folder `{folder}`" + '\n' + str(content[0]))
        logger.debug(f"Change work folder to {folder}")

    def get_folders(self, ffilter: t.Callable = None, transfer: t.Callable = None) -> t.List:
        """
        Args:
            ffilter: 过滤文件夹名称规则
            transfer: 格式化文件夹名称规则

        Returns: List[str]
        """

        status, folders = self.connection.list()

        if ffilter is None and transfer is None:
            return folders
        else:
            ffilter = ffilter or str
            transfer = transfer or str
            folders = [transfer(folder) for folder in folders if ffilter(folder)]
            return folders

    def get_uid(self, folder: str, start: int = '1', end='*') -> t.List:
        logger.info(f"Query UID info from folder {folder} by indexes from {start} to {end}.")
        self._change_workfolder(folder)
        status, content = self.connection.uid('SEARCH', f"{start}:{end}")  # RFC3501 6.4.8 UID Command
        if status_is_ok(status):
            got_uids = list(map(lambda uid: int(uid), split_uid(content)))
            if got_uids:
                logger.info(f"Get UID from {got_uids[0]} to {got_uids[-1]}, total {len(got_uids)} uid numbers.")
            else:
                logger.info(f"Get nothing about uid.")
            return got_uids
        raise IMAP4.error(f"Failed to query UID info from folder {folder}")

    def get_mail_by_uid(self, folder: str, uid: t.Union[int, str]) -> MailEntity:
        logger.info(f"Query mail content from folder {folder} by UID {uid}")
        self._change_workfolder(folder)

        status, response = self.connection.uid('FETCH', str(uid), '(RFC822)')
        if status_is_ok(status) and response_is_ok(response):
            return built_entity(self.username, folder, uid, response)
        status, response = self.connection.fetch(str(uid), '(BODY.PEEK[])')
        if status_is_ok(status) and response_is_ok(response):
            return built_entity(self.username, folder, uid, response)
        if status_is_ok(status) and not response_is_ok(response):
            raise IMAP4.error(f"UID {uid} is invalid in folder {folder}")
        raise IMAP4.error(f"Failed to query mail of UID {uid} content from folder {folder}")


class SMTPTransport(object):

    def __init__(self, host: str,
                 port: int = None,
                 ssl: bool = True,
                 ssl_context: pythonssllib.SSLContext = None,
                 starttls: bool = False):
        self.host = host
        self.ssl = ssl
        self.ssl_context = ssl_context
        self.starttls = starttls
        if ssl:
            self.port = port or smtplib.SMTP_SSL_PORT
            if ssl_context is None:
                ssl_context = pythonssllib.create_default_context()
            self.server = smtplib.SMTP_SSL(self.host, self.port, context=ssl_context)
        else:
            self.port = port or smtplib.SMTP_PORT
            self.server = smtplib.SMTP(self.host, self.port)

        if starttls:
            self.server.starttls()
        logger.info(f"Created SMTP transport for {self.host}:{self.port}")

    def connect(self, username: str, password: str):
        self.server.login(username, password)
        logger.info(f"Logged into server {self.host} and selected mailbox 'INBOX'")
        return self.server


class SMTPBox(object):

    def __init__(self, host: str,
                 port: int = None,
                 username: str = None,
                 password: str = None,
                 ssl: bool = True,
                 ssl_context: pythonssllib.SSLContext = None,
                 starttls=False):

        self.server = SMTPTransport(host, port, ssl, ssl_context, starttls)

        self.username = username
        self.password = password

        self.connection = self.server.connect(self.username, self.password)

        logger.info(f"Connected to SMTP Server with user {username} on {host}{' over SSL' if ssl or starttls else ''}")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.logout()

    def logout(self):
        self.connection.close()
        logger.info(f"Disconnected from SMTP Server {self.server.host}@{self.username}")

    def reconnect(self):
        self.server = SMTPTransport(self.server.host, self.server.port,
                                    self.server.ssl, self.server.ssl_context, self.server.starttls)
        self.connection = self.server.connect(self.username, self.password)

    def _pack(self, **kwargs):
        mail = MIMEMultipart()
        mail['Subject'] = kwargs.get('subject', __package__)

        send_to = kwargs.get('To', kwargs.get('to'))
        if isinstance(send_to, list):
            send_to = ';'.join(send_to)
        if not send_to:
            raise ValueError("recipients info should be referred.")
        mail['To'] = send_to

        send_cc = kwargs.get('cc', kwargs.get('CC', ''))
        if isinstance(send_cc, list):
            send_cc = ';'.join(send_cc)
        mail['CC'] = send_cc

        from_ = kwargs.get('from_', None) or self.username
        mail['From'] = from_

        attachments = kwargs.get('attachments')
        if attachments:
            attachments = _sort_attach(attachments)
            [mail.attach(attach) for attach in attachments]

        text = kwargs.get('text')
        if text:
            text = MIMEText(text)
            mail.attach(text)

        html = kwargs.get('html')
        if html:
            html = MIMEText(html, 'html')
            mail.attach(html)
        return mail

    def send(self, subject, recipients, cc=None, text=None, html=None, from_=None, attachments=None):
        """
        Args:
            subject: 邮件主题/标题
            recipients(Optional[list, str]): 收件人
            cc(Optional[list, str]):
            text(str):纯文本邮件文本信息
            html(str): html形式的邮件文本信息
            from_(str): 发件人信息
            attachments(list): 附件路径
        """
        msg = self._pack(subject=subject, to=recipients, cc=cc, from_=from_,
                         text=text, html=html, attachments=attachments)
        from_ = from_ or self.username
        self.connection.sendmail(from_, recipients, msg.as_string())
        logger.info(f"Send email to {recipients} and copy to {cc} titled [{subject}].")


