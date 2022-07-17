-- SQL 脚本限定 MySQL 数据库使用, 暂未考虑适配其他 SQL 数据库

CREATE DATABASE settlements;
USE settlements;

-- ==================================================================
-- 用于记录邮件文件中股票对账单的解析结果
--
-- @fogname: 处理基于 file_preprocess 表的 fogname 字段记录
-- ==================================================================
CREATE TABLE IF NOT EXISTS stock_tradeorder_result (
    fogname               VARCHAR(100)  NOT NULL  COMMENT '邮件文件唯一标识, 来自于 email 库中的 mail_files 表的 fogname 字段',
    stock_account         VARCHAR(50)   NOT NULL  COMMENT '股票账户',
    trade_date            DATE          NOT NULL  COMMENT '交易日期',
    total_assets          DECIMAL(18,3) NOT NULL  COMMENT '总资产',
    total_market_value    DECIMAL(18,3) NOT NULL  COMMENT '总市值',
    net_assets            DECIMAL(18,3) NOT NULL  COMMENT '净资产',
    total_liabilities     DECIMAL(18,3) NOT NULL  COMMENT '总负债',
    financing_liabilities DECIMAL(18,3) NOT NULL  COMMENT '融资负债',
    bonded_liabilities    DECIMAL(18,3) NOT NULL  COMMENT '债券负债',
    bonded_interest       DECIMAL(18,3) NOT NULL  COMMENT '债券利息',
    available_balance     DECIMAL(18,3) NOT NULL  COMMENT '可用余额',
    trade_count           INT(11)       NOT NULL  COMMENT '总成交笔数记录(不准确,可能存在融合交易记录导致交易记录比实际成交笔数要少)',
    parse_time            DATETIME      NOT NULL  COMMENT '解析时间',
    remark                VARCHAR(100)  NOT NULL  COMMENT '备注',
    PRIMARY KEY (fogname)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


-- ==================================================================
-- 用于记录邮件文件中估值表的单一数据的解析结果
--
-- @fogname: 处理基于 file_preprocess 表的 fogname 字段记录
-- @product_name: 产品名称可能会发生变化, 可能是运营提出的对产品名称做出改变, 也可能托管方对产品名称做出改变(实际名称不变, 解析结果发生改变)
-- ==================================================================
CREATE TABLE IF NOT EXISTS valuation_result (
    fogname                   VARCHAR(100)  NOT NULL  COMMENT '邮件文件唯一标识, 来自于 email 库中的 mail_files 表的 fogname 字段',
    product_name              VARCHAR(255)  NOT NULL  COMMENT '产品名称',
    valuation_date            DATE          NOT NULL  COMMENT '估值日期',
    unit_netvalue             DECIMAL(18,3) NOT NULL  COMMENT '单位净值',
    accumulated_netvalue      DECIMAL(18,3) NOT NULL  COMMENT '累计净值',
    unit_netvalue_adj         DECIMAL(18,3)           COMMENT '复权单位净值',
    accumulated_netvalue_adj  DECIMAL(18,3)           COMMENT '复权累计净值',
    total_assets              DECIMAL(18,3) NOT NULL  COMMENT '资产合计金额',
    total_liabilities         DECIMAL(18,3) NOT NULL  COMMENT '负债合计金额',
    net_assets                DECIMAL(18,3) NOT NULL  COMMENT '资产净值金额',
    invest_in_securities      DECIMAL(18,3)           COMMENT '证券投资合计金额',
    invest_in_stock           DECIMAL(18,3)           COMMENT '股票投资合计金额',
    negotiable_shares         DECIMAL(18,3)           COMMENT '可流通股票金额',
    negotiable_sz_shares      DECIMAL(18,3)           COMMENT '深市可流通股票金额',
    negotiable_sh_shares      DECIMAL(18,3)           COMMENT '沪市可流通股票金额',
    invest_in_derivative      DECIMAL(18,3)           COMMENT '衍生工具投资合计金额',
    invest_in_bond            DECIMAL(18,3)           COMMENT '债券投资合计金额',
    invest_in_fund            DECIMAL(18,3)           COMMENT '基金投资合计金额',
    available_positions       DECIMAL(18,3)           COMMENT '可用头寸',
    parse_time                DATETIME      NOT NULL  COMMENT '解析时间',
    remark                    VARCHAR(100)  NOT NULL  COMMENT '备注',
    PRIMARY KEY (fogname, product_name, valuation_date, parse_time)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- ==================================================================
-- 用于记录科目项信息, 一一对应产品, 可能对于某一个产品来说, 该项目名称是特指的
-- 该表暂时考虑只存储一二三级科目项信息，四级科目数据量过于庞大, 暂不考虑采用普通 SQL 表结构来存储
-- 对于规模较小的私募机构可以考虑用该表来存储所有科目项信息
--
-- @fogname: 处理基于 file_preprocess 表的 fogname 字段记录
-- @map_subject_name: 对于资管券商给定的科目名称可能不符合内部统计规范, 需要做统一映射,
--                    例如可能某一科目项在内部是一级科目， 但资管券商设定的科目名称是二级科目, 因此需要做映射
-- ==================================================================
CREATE TABLE IF NOT EXISTS subject_item (
    fogname                   VARCHAR(100)  NOT NULL  COMMENT '邮件文件唯一标识, 来自于 email 库中的 mail_files 表的 fogname 字段',
    product_name              VARCHAR(255)  NOT NULL  COMMENT '产品名称',
    raw_subject_code          VARCHAR(255)  NOT NULL  COMMENT '原始科目代码数据',
    subject_code              VARCHAR(255)  NOT NULL  COMMENT '科目代码',
    raw_subject_name          VARCHAR(255)  NOT NULL  COMMENT '原始科目名称数据',
    subject_name              VARCHAR(255)  NOT NULL  COMMENT '科目名称',
    map_subject_name          VARCHAR(255)  NOT NULL  COMMENT '映射统一科目名称',
    subject_level             TINYINT       NOT NULL  COMMENT '科目级别(一般情况只有1/2/3/4)',
    parse_time                DATETIME      NOT NULL  COMMENT '解析时间',
    remark                    VARCHAR(100)  NOT NULL  COMMENT '备注',
    PRIMARY KEY (fogname, product_name, raw_subject_code, raw_subject_name),
    INDEX (product_name, map_subject_name)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;



