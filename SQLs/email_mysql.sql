-- SQL 脚本限定 MySQL 数据库使用, 暂未考虑适配其他 SQL 数据库

CREATE DATABASE IF NOT EXISTS emails;
USE emails;

-- ==================================================================
-- 用于管理邮箱账户, 结算邮箱可能有多个账户
--
-- 暂时没有考虑好密码应该怎么存储, 可能是加密的, 或者是明文的
-- 总体来说, 明文更方便, 而且是内部管理使用的密码, 数据库不接入互联网
-- 考虑明文是因为密码还需要用来登录爬取邮件的
-- ==================================================================
CREATE TABLE IF NOT EXISTS email_accounts (
  email_id      INT          NOT NULL   AUTO_INCREMENT  COMMENT '邮箱账户内部管理ID',
  email         VARCHAR(255) NOT NULL                   COMMENT '邮箱账户',
  password      VARCHAR(255)                            COMMENT '邮箱密码',
  register_time DATETIME     NOT NULL                   COMMENT '注册时间',
  logout_time   DATETIME                                COMMENT '注销时间',
  status        TINYINT(1)   NOT NULL   DEFAULT 0       COMMENT '邮箱账户状态, 0: 正常, 1: 注销, 2: 停用, 3: 删除(一般不会删除)',
  PRIMARY KEY (email_id)
);

-- ==================================================================
-- 用于管理邮箱账户的接收邮件摘要信息, 作为元数据管理方便查找邮件
--
--   @box: 用户理解是 folder, 是邮箱文件夹
--   @uid: 邮箱中唯一标识的值, 仅限定在某一 box 中唯一
--
--   邮件存在发送人邮箱(服务器)发送时间和接收者邮箱(服务器)收到的时间
--   @sendtime: 跟据邮箱数据中 Received 字段获取最早时间
--   @recvtime: 跟据邮箱数据中 Received 字段获取最晚时间
-- ==================================================================
CREATE TABLE IF NOT EXISTS mails_summary(
    mail_id    INT           NOT NULL   AUTO_INCREMENT  COMMENT '邮件内部管理ID',
    email_id   INT           NOT NULL   COMMENT '邮箱账户内部管理ID',
    box        VARCHAR(50)   NOT NULL   COMMENT '邮箱文件夹',
    uid        INT           NOT NULL   COMMENT '邮件UID',
    subject    VARCHAR(2048) NOT NULL   COMMENT '邮件标题/主题',
    sender     VARCHAR(100)  NOT NULL   COMMENT '邮件发送人',
    recipients VARCHAR(5000) NOT NULL   COMMENT '邮件收件人',
    cc         VARCHAR(5000) DEFAULT '' COMMENT '邮件抄送人',
    sendtime   DATETIME      NOT NULL   COMMENT '邮件发送时间',
    recvtime   DATETIME      NOT NULL   COMMENT '邮件接收时间',
    PRIMARY KEY (mail_id),
    INDEX (email_id, box, uid),
    FOREIGN KEY (email_id) REFERENCES email_accounts(email_id) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- ==================================================================
-- 邮件爬取落地存储器管理, 落地存储可能有多种方式, 为了容灾也好, 方便多应用适配也好

-- @storage_type: S3: s3, Linux 文件系统: localhost
-- @storage_path: 落地存储路径, 对于 Linux 系统是绝对路径; 对于类 S3 存储是 bucket 名称
-- ==================================================================
CREATE TABLE IF NOT EXISTS mail_storages(
    storage_id   INT            NOT NULL AUTO_INCREMENT COMMENT '存储器ID',
    storage_type VARCHAR(255)   NOT NULL                COMMENT '存储器类型',
    storage_ip   VARCHAR(255)   NOT NULL                COMMENT '存储器连接IP',
    storage_port INT            NOT NULL                COMMENT '存储器连接端口',
    storage_user VARCHAR(255)   NOT NULL                COMMENT '存储器登录用户名',
    storage_pass VARCHAR(255)   NOT NULL                COMMENT '存储器登录密码',
    storage_path VARCHAR(255)   NOT NULL                COMMENT '存储器路径',
)

-- ==================================================================
-- 用于管理邮箱账户的接收邮件附件信息, 作为元数据管理方便查找附件文件
--
-- @box: 为了不必要的麻烦, 请务必使用英文字母创建邮箱文件夹
-- ==================================================================
CREATE TABLE IF NOT EXISTS mails_files(
    email_id      INT          NOT NULL     COMMENT '邮箱内部管理ID',
    box           VARCHAR(30)  NOT NULL     COMMENT '邮箱文件夹',
    uid           INT          NOT NULL     COMMENT '邮件UID',
    fogname       VARCHAR(100)              COMMENT '文件存储名称({email_id}_{box}_{uid}_{md5[:5]}.{ext})',
    original_name VARCHAR(1000)NOT NULL     COMMENT '文件原名称',
    storage_id    INT          NOT NULL     COMMENT '存储器ID',
    filesize      INT                       COMMENT '文件大小',
    PRIMARY KEY (fogname),
    INDEX (email_id, box, uid),
    FOREIGN KEY (email_id, box, uid)
        REFERENCES mails_summary (email_id, box, uid),
    FOREIGN KEY (storage_id)
        REFERENCES mail_storages(storage_id) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- ==================================================================
-- 下载失败的邮件信息储存,为了能够溯源错误以及重新下载
-- ==================================================================
CREATE TABLE IF NOT EXISTS error_download(
    error_id   INT          NOT NULL AUTO_INCREMENT COMMENT '错误ID',
    email_id   VARCHAR(100) NOT NULL                COMMENT '邮箱内部管理ID',
    box        VARCHAR(30)  NOT NULL                COMMENT '邮箱文件夹',
    uid        INT          NOT NULL                COMMENT '邮件UID',
    error_time DATETIME     NOT NULL                COMMENT '发生错误的时间',
    error_msg  TEXT                                 COMMENT '运行错误信息',
    redownload TINYINT(1)   NOT NULL DEFAULT 0      COMMENT '是否已经重新下载; 0: 未重新下载, 1: 已重新下载',
    ignore_err TINYINT(1)   NOT NULL DEFAULT 0      COMMENT '是否忽略错误; 0: 否, 1: 是',
    INDEX (email_id, box, uid)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


-- ==================================================================
-- 用于邮件文件预处理记录, 判定邮件相关文件是否属于某个文件类型
-- 只有当文件被某一预处理文件处理过后, 才会被记录在这里
--
-- @fogname: 邮件文件唯一标识, 来自于 email 库中的 mail_files 表的 fogname 字段
-- ==================================================================
CREATE TABLE IF NOT EXISTS file_preprocess (
    fogname                     VARCHAR(100) NOT NULL                               COMMENT '邮件文件唯一标识, 来自于 email 库中的 mail_files 表的 fogname 字段',
    is_valuation                TINYINT(1)   NOT NULL DEFAULT 0                     COMMENT '是否为估值表文件',
    is_stocktradeorder          TINYINT(1)   NOT NULL DEFAULT 0                     COMMENT '是否为股票成交对账单文件',
    is_futuretradeorder         TINYINT(1)   NOT NULL DEFAULT 0                     COMMENT '是否为期货成交对账单文件',
    is_optionsorder             TINYINT(1)   NOT NULL DEFAULT 0                     COMMENT '是否为期权成交对账单文件',
    check_valuation_time        DATETIME     NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '估值表文件的预处理时间',
    check_stocktradeorder_time  DATETIME     NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '股票成交对账单文件的预处理时间',
    check_futuretradeorder_time DATETIME     NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '期货成交对账单文件的预处理时间',
    check_optionsorder_time     DATETIME     NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '期权成交对账单文件的预处理时间',
    PRIMARY KEY (fogname)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;