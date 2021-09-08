# coding=utf8

import chardet
import imghdr
import os
import time
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from X1.stand import ArgStandError


def uid_rules(start, end):
    start = int(start)
    if start < 1:
        raise ArgStandError("Illegal start uid, start uid smaller than 1")
    if end != '*':
        end = int(end)
        if end < start:
            raise ArgStandError("Illegal end uid, end uid could not small more than start uid")
    elif end == '*':
        pass
    else:
        raise ArgStandError("What the fucking arguments you did??????????????????????? outrageous and ridiculous")
    return start, end


def split_uid(raw):
    return raw[0].decode('utf-8').split()


def default_extract_folder(raw):
    raw = str(raw)
    return (raw.split('"/"')[-1]
               .replace("\"", "")
               .strip())


def status_is_ok(status):
    return status == 'OK'


def response_is_ok(content):
    return (content is not None) and \
           (content[0] is not None)


def decode_mail_string(string, encode=None, error=None):
    try:
        if isinstance(string, str):
            string = string.encode("utf8")
        elif encode is not None:
            try:
                string = str(string, encode)
            except UnicodeDecodeError:
                if encode.lower() == 'gb2312':
                    encode = 'GB18030'
                    string = str(string, encode, errors='replace')
                else:
                    string = str(string, encode, errors='replace')
        else:
            chartype = chardet.detect(string)["encoding"]
            if chartype is not None:
                if error:
                    string = string.decode(chartype, errors=error).encode("utf8")
                else:
                    string = string.decode(chartype).encode("utf8")
            else:
                if error:
                    string = string.decode("GB18030", errors=error).encode("utf8")
                else:
                    string = string.decode("GB18030").encode("utf8")
    except UnicodeDecodeError as e:
        if 'gb2312' in e:
            if error:
                string = string.decode('GB18030', errors=error).encode("utf8")
            else:
                string = string.decode('GB18030').encode("utf8")

    return string


def _package_image(filename, imagedata):
    if imghdr.what(None, imagedata[:32]):
        image = MIMEImage(imagedata)
        image.add_header('Content-ID', filename)
        return image


def _sort_attach(paths):
    attaches = []
    for path in paths:
        with open(path, 'rb') as rd:
            raw_file = rd.read()
            filename = os.path.split(path)[-1]
            image = _package_image(filename, raw_file)
            if image is not None:
                attaches.append(image)
            else:
                attach = MIMEApplication(raw_file, Name=filename)
                attaches.append(attach)
    return attaches


def restart_connection(box, sleeptime=60):
    if not sleeptime:
        return
    time.sleep(sleeptime)
    box.reconnect()

