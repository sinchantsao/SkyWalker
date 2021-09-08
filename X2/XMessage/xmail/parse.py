# coding=utf8

import base64
import quopri
import re
import typing as t
from datetime import datetime
from email import message_from_string
from email.header import decode_header
from email.utils import parseaddr, parsedate
from X1.stand import ParamStandError
from X2.XMessage.xmail.utils import decode_mail_string
from X2.XMessage.xmail.container import MailContext, MailFile, Attachment, Attachments, MailEntity


def match_user_account(account_string: str):
    """
    Args:
        account_string:
          type 1:
            '"=?<charset>?<encoding>?<encoded-text>?=" <example@example.com>'
          type 2:
            'example@example.com'
    Returns:
        'example@example.com'
    """
    try:
        account = re.findall("<(.*)?>", account_string)[0]
    except IndexError:
        account = account_string.strip()
    return account


def split_multimailuser(msg):
    if not msg:
        return []
    return list(map(match_user_account, msg.split(',')))


def encoded_words_to_text(encoded_words: str):
    encoded_word_regex = r'"?=\?{1}(.+)\?{1}([B|Q])\?{1}(.+)\?{1}="?'
    try:
        charset, encoding, encoded_text = re.match(encoded_word_regex, encoded_words).groups()
    except AttributeError:
        raise ParamStandError(f"Encode word does not match with regex: {encoded_word_regex}")
    if encoding == 'B':
        byte_string = base64.b64decode(encoded_text)
    elif encoding == 'Q':
        byte_string = quopri.decodestring(encoded_text)
    else:
        raise ParamStandError(f"Encode word does not match with regex: {encoded_word_regex}")
    return byte_string.decode(charset)

def extract_subject(msg):
    subject = msg.get('subject')
    decoded_pairs = decode_header(subject)
    chars = []
    for bstring, charset in decoded_pairs:
        if isinstance(bstring, str):
            chars.append(bstring)
            continue
        if charset is not None:
            sstring = decode_mail_string(bstring, charset)
            chars.append(sstring)
    subject = ''.join(chars)
    return re.sub('\r\n\t', '', subject)


def extract_sender(msg):
    sender = msg.get('from')
    return parseaddr(sender)[-1]


def extract_carboncopies(raw):
    raw_info = raw.get('cc', '')
    carboncopies = split_multimailuser(raw_info)
    return ';'.join(carboncopies)


def extract_recipients(msg):
    recipients = msg.get('to', '')
    recipients = split_multimailuser(recipients)
    return ';'.join(recipients)


def extract_times(msg):
    received_fields = msg.get_all('Received', [])
    recvtime_list = []
    for recv_info in received_fields:
        forinfo = recv_info.split(';')[-1].strip()
        timeinfo = (re.sub(pattern='[\r\t\n]', repl='', string=forinfo)[:31])
        time = parsedate(timeinfo)
        recvtime_list.append(time)
    if recvtime_list:
        recvtime_list = sorted(recvtime_list)
        sendtime, recvtime = recvtime_list[0], recvtime_list[-1]
    else:
        sendtime = recvtime = parsedate(msg.get('date'))

    return datetime(*sendtime[:6]), datetime(*recvtime[:6])


def fetch_context(msg):
    context = []
    for subpart in msg.walk():
        part_type = subpart.get_content_type()
        if part_type in ("text/html", "text/plain"):
            try:
                content = decode_mailcontext(subpart).encode('utf-8')
            except UnicodeDecodeError:
                content = decode_mailcontext(subpart).encode('gb18030')
            context.append(content)
    return context


def pull_attachments(msg):
    for subpart in msg.walk():
        encodename = subpart.get_filename()
        if encodename is not None:
            filename = decode_header(encodename)[0]
            filename = decode_mail_string(*filename)
            fileflow = subpart.get_payload(decode=True)
            if fileflow:
                attach = MailFile(filename, fileflow)
            else:
                attach = MailFile(filename, fileflow, 0)
            yield attach


def decode_mailcontext(content):
    # text = ""
    # encode_typ = content.get('Content-Transfer-Encoding', None)
    #
    # if encode_typ == "7bit":
    #     try:
    #         payload = content.get_payload()
    #         text = quopri.decodestring(payload)
    #         text = decode_mail_string(text)
    #     except ValueError as value_err:
    #         if "string argument should contain only ASCII characters" in str(value_err):
    #             text = payload
    #
    # elif encode_typ == "quoted-printable":
    #     fn = content.get_filename()
    #     if fn is None:
    #         text = quopri.decodestring(content.get_payload())
    #         text = decode_mail_string(text)
    #     # else:
    #     #     self.fileContentPart(contentPart)
    #
    # elif encode_typ == "base64":
    #     text = base64.decodebytes(content.get_payload().encode('utf8'))
    #     try:
    #         text = decode_mail_string(text)
    #     except UnicodeDecodeError as e:
    #         logger.warn('Cannot decode xmail context, replace error chars')
    #         text = decode_mail_string(text, error='replace')
    #
    # elif encode_typ is None:
    #     text = content.get_payload()
    #     text = decode_mail_string(text)
    #
    # else:
    #     logger.warn("Unknown Content-Transfer-Encoding: '{}'".format(encode_typ))
    #     # TODO notify
    text = content.get_payload()

    return text


def built_entity(account: str, box: str, uid: int,
                 response: t.List) -> MailEntity:
    protocol, msg = response[0]
    try:
        msg = msg.decode('utf-8')
    except UnicodeDecodeError:
        msg = msg.decode('GB18030', errors='replace')
    msg = message_from_string(msg)
    subject = extract_subject(msg)
    sender = extract_sender(msg)
    carboncopies = extract_carboncopies(msg)
    recipients = extract_recipients(msg)
    sendtime, recvtime = extract_times(msg)
    context = fetch_context(msg)
    mailcontext = MailContext(account, box, uid, subject,
                              sender, recipients, carboncopies,
                              sendtime, recvtime, context)
    attachments = [Attachment(account, box, uid, subject,
                              sender, recipients, carboncopies,
                              sendtime, recvtime, packfile=attach)
                   for attach in pull_attachments(msg)]
    return MailEntity(mailcontext, Attachments(*attachments),
                      account=account, box=box, uid=uid, subject=subject,
                      sender=sender, recipients=recipients, carboncopies=carboncopies,
                      sendtime=sendtime, recvtime=recvtime)


