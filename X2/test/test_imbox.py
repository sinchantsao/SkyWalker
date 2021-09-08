# coding=utf-8

from X2.XMessage.xmail.utils import default_extract_folder
from X2.XMessage.xmail.connect import IMAPBox


if __name__ == '__main__':

    hostname = 'imap.exmail.qq.com'
    username = ''
    password = ''

    mail_folder = ''
    mail_uid = ''

    s3_storage_bucket = ''
    s3_storage_loc_prefix = ''

    storage_filepath = ''

    # ==============================================================================
    # connection
    box = IMAPBox(hostname=hostname,
                  username=username,
                  password=password)
    # ==============================================================================
    # xmail query folders
    folders = box.get_folders(transfer=default_extract_folder)

    # ==============================================================================
    # xmail query uids
    uids = box.get_uid(mail_folder)
    print(f"UID starts at {uids[0]}, ends at {uids[-1]}")

    # ==============================================================================
    # xmail query uid
    if mail_folder and mail_uid:
        mail = box.get_mail_by_uid(mail_folder, mail_uid)
    # ==============================================================================
    # xmail storage
        if s3_storage_bucket:
            mail.write_to_ceph(bucket=s3_storage_bucket, prefix=s3_storage_loc_prefix)
        if storage_filepath:
            mail.write_to_unix(storage_filepath)

        print(mail)
