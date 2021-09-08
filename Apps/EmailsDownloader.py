# !/usr/bin/python
# coding=utf8
"""

box => folder

box 和 folder 是同一个概念
box     => 邮箱协议中的概念
folder  => 邮箱用户理解

"""

import logging
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from X2.utlis import create_dir
from X2.XMessage.xmail.connect import IMAPBox
from X2.XMessage.xmail.auto import ProduceUID, UIDDownloader


if __name__ == '__main__':

    import argparse

    argsparser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    argsparser.add_argument("-u", "--username", required=True, help="email username.")
    argsparser.add_argument("-p", "--password", required=True, help="email password.")
    argsparser.add_argument("--box", default=None, nargs='+', help="email box(folder)s to download.")
    argsparser.add_argument("--host", default="imap.exmail.qq.com", help="imap server host.")
    argsparser.add_argument("--sqlite-db", default=None, help="sqlite database for emails summary info.")
    argsparser.add_argument("--threads", default=4, type=int, help="thread number for downloading emails.")
    argsparser.add_argument("--save-to-ceph", action="store_true", help="saving email to ceph or not.")
    argsparser.add_argument("--ceph-bucket", type=str, required="--save-to-ceph" in sys.argv, help="s3 bucket name.")
    argsparser.add_argument("--save-to-avenger", action="store_true", help="saving email to avenger or not.")
    argsparser.add_argument("--avenger-source", type=str, required="--save-to-avenger" in sys.argv, help="avenger source name.")
    argsparser.add_argument("--save-to-localhost", action="store_true", help="saving email to localhost or not.")
    argsparser.add_argument("--localhost-directory", type=str, required="--save-to-localhost" in sys.argv, help="localhost directory path.")

    args = argsparser.parse_args()

    log_directory = create_dir(os.environ.get("X2_MAIL_LOGS", "~/email_logs"))
    logfile_name_format = os.path.join(log_directory, args.username)
    stream_log_handler = StreamHandler()
    stream_log_handler.setLevel(logging.DEBUG)
    timing_log_handler = TimedRotatingFileHandler(filename=logfile_name_format,
                                                  when='H', interval=12)
    timing_log_handler.setLevel(logging.DEBUG)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(threadName)10s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[stream_log_handler, timing_log_handler]
    )

    boxes = [IMAPBox(hostname=args.host,
                     username=args.username,
                     password=args.password)
             for n in range(args.threads)]

    uid_downloader = [
        UIDDownloader(imap_box=box,
                      save_to_ceph=args.save_to_ceph, bucket=args.ceph_bucket,
                      sqlite_db=args.sqlite_db,)
        for box in boxes
    ]
    [ud.start() for ud in uid_downloader]

    uid_producer = ProduceUID(
        imap_box=IMAPBox(hostname=args.host, username=args.username, password=args.password),
        boxes=args.box
    )
    uid_producer.start()

