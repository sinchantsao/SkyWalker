# coding=utf8
"""

DESTINATION:
    同步 SQLite / MySQL 数据库

NOTE:
    采用IDE运行不会正常显示同步进度

"""

from X2.XMessage.xmail.record import init_records, SQLServerType

if __name__ == '__main__':
    mysql_host = "192.168.1.195"
    mysql_port = 30233
    mysql_db = "emails"
    mysql_user = "root"
    mysql_password = "wqsettle"
    sync2point = SQLServerType.SQLite

    init_records(
        sync2point=sync2point,
        mysql_location=(mysql_host, mysql_port, mysql_db, mysql_user, mysql_password),
    )
