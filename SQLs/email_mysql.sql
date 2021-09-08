CREATE DATABASE IF NOT EXISTS emails;
USE emails;

# ==================================================================
#   @box: 用户理解是folder,是邮箱文件夹
#   @uid: 邮箱中唯一标识的值,仅限定在某一box中唯一
#
#   邮件存在发送人邮箱(服务器)发送时间和接收者邮箱(服务器)收到的时间
#   @sendtime: 跟据邮箱数据中Received字段获取最早时间
#   @recvtime: 跟据邮箱数据中Received字段获取最晚时间
# ==================================================================
CREATE TABLE IF NOT EXISTS mails_summary(
    user       VARCHAR(100)  NOT NULL   COMMENT '邮箱账户名称(不包含域名/邮箱厂商)',
    box        VARCHAR(50)   NOT NULL   COMMENT '邮箱文件夹',
    uid        INT           NOT NULL   COMMENT '邮件UID',
    subject    VARCHAR(2048) NOT NULL   COMMENT '邮件标题/主题',
    sender     VARCHAR(100)  NOT NULL   COMMENT '邮件发送人',
    recipients VARCHAR(5000) NOT NULL   COMMENT '邮件收件人',
    cc         VARCHAR(5000) DEFAULT '' COMMENT '邮件抄送人',
    sendtime   DATETIME      NOT NULL   COMMENT '邮件发送时间',
    recvtime   DATETIME      NOT NULL   COMMENT '邮件接收时间',
    PRIMARY KEY (user, box, uid)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

# ==================================================================
#   @fogname: 最好能保证这一值能够唯一
#   @storage_type: 文件存储的存储器类型
#       1. ceph
#       2. avenger
#       3. localhost(default)
#   @storage_point: 在存储器中的位置,根据不同存储器有不同的理解
#       1. 对于ceph(类s3存储)存储则为定位前缀,即bucket+用户自定义路径
#       2. 对于Avenger存储则为Source名称
#       3. 对于服务器本地存储则为绝对路径文件夹
# ==================================================================
CREATE TABLE IF NOT EXISTS mails_files(
    user          VARCHAR(100) NOT NULL     COMMENT '邮箱账户名称(不包含域名/邮箱厂商)',
    box           VARCHAR(30)  NOT NULL     COMMENT '邮箱文件夹',
    uid           INT          NOT NULL     COMMENT '邮件UID',
    fogname       VARCHAR(100)              COMMENT '文件存储名称(user_box_uid_md5[:5].ext)',
    original_name VARCHAR(1000) NOT NULL    COMMENT '文件原名称',
    storage_type  VARCHAR(50)  NOT NULL     COMMENT '存储形式名称/标记',
    storage_point VARCHAR(100) NOT NULL     COMMENT '存储位置定位',
    PRIMARY KEY (storage_type, storage_point, fogname),
    FOREIGN KEY (user, box, uid)
        REFERENCES mails_summary (user, box, uid)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

# ==================================================================
# 下载失败的邮件信息储存,为了能够溯源错误以及重新下载
# ==================================================================
CREATE TABLE IF NOT EXISTS error_download(
    user      VARCHAR(100) NOT NULL COMMENT '邮箱账户名称(不包含域名/邮箱厂商)',
    box       VARCHAR(30)  NOT NULL COMMENT '邮箱文件夹',
    uid       INT          NOT NULL COMMENT '邮件UID',
    error_msg TEXT,
    PRIMARY KEY (user, box, uid)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;
