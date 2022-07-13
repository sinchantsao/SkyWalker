-- SQL 脚本限定 MySQL 数据库使用, 暂未考虑适配其他 SQL 数据库

CREATE DATABASE settlements;
USE settlements;

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

-- ==================================================================
-- 用于记录邮件文件中股票对账单的解析结果

-- @fogname: 处理基于 file_preprocess 表的 fogname 字段记录
-- ==================================================================
CREATE TABLE IF NOT EXISTS stock_tradeorder_result (
    fogname               VARCHAR(100)  NOT NULL  COMMENT '邮件文件唯一标识, 来自于 email 库中的 mail_files 表的 fogname 字段',
    stock_account         VARCHAR(50)   NOT NULL  COMMENT '股票账户',
    trade_date            DATE          NOT NULL  COMMENT '交易日期',
    total_assets          DECIMAL(18,3) NOT NULL  COMMENT '总资产',
    total_maket_value     DECIMAL(18,3) NOT NULL  COMMENT '总市值',
    net_assets            DECIMAL(18,3) NOT NULL  COMMENT '净资产',
    total_liabilities     DECIMAL(18,3) NOT NULL  COMMENT '总负债',
    financing_liabilities DECIMAL(18,3) NOT NULL  COMMENT '融资负债',
    bonded_liabilities    DECIMAL(18,3) NOT NULL  COMMENT '债券负债',
    bonded_interest       DECIMAL(18,3) NOT NULL  COMMENT '债券利息',
    available_balance     DECIMAL(18,3) NOT NULL  COMMENT '可用余额',
    trade_count           INT(11)       NOT NULL  COMMENT '总成交笔数记录(不准确,可能存在融合交易记录导致交易记录比实际成交笔数要少)',
    parse_time            DATETIME      NOT NULL  COMMENT '解析时间',
    comment               VARCHAR(100)  NOT NULL  COMMENT '备注',
    PRIMARY KEY (fogname)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


-- ==================================================================
-- 用于记录邮件文件中估值表的解析结果
--
-- @fogname: 处理基于 file_preprocess 表的 fogname 字段记录
-- @product_name: 产品名称可能会发生变化, 可能是运营对产品名称做出改变, 也可能托管方对产品名称做出改变(实际名称不变, 解析结果发生改变)
-- ==================================================================
CREATE TABLE IF NOT EXISTS valuation_result (
    fogname                   VARCHAR(100)  NOT NULL  COMMENT '邮件文件唯一标识, 来自于 email 库中的 mail_files 表的 fogname 字段',
    product_name              VARCHAR(255)  NOT NULL  COMMENT '产品名称',
    valuation_date            DATE          NOT NULL  COMMENT '估值日期',
    unit_netvalue             DECIMAL(18,3) NOT NULL  COMMENT '单位净值',
    accumulated_netvalue      DECIMAL(18,3) NOT NULL  COMMENT '累计净值',
    unit_netvalue_adj         DECIMAL(18,3)           COMMENT '复权单位净值',
    accumulated_netvalue_adj  DECIMAL(18,3)           COMMENT '复权累计净值',
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;