CREATE DATABASE file_tendencies;
USE file_tendencies;

# ==================================================================
# 发现文件是否为对账单文件
# 以防检查程序中断/错误,在检查程序一开始就应该写入需要处理的信息
# ==================================================================
CREATE TABLE IF NOT EXISTS find_statements(
    id              INT          PRIMARY KEY,
    channel         VARCHAR(50)  NOT NULL COMMENT '收到处理消息的频道',
    fogname         VARCHAR(100) NOT NULL COMMENT '文件唯一标识',
    storage_type    VARCHAR(50)  NOT NULL COMMENT '存储器',
    storage_point   VARCHAR(100) NOT NULL COMMENT '存储位置',
    is_statement    TINYINT      COMMENT '是否为对账单文件' # 0 => 否; 1 => 是; -1 => 检查程序出问题没有给出结果
);

# ==================================================================
# 发现文件是否为估值表文件
# 以防检查程序中断/错误,在检查程序一开始就应该写入需要处理的信息
# ==================================================================
CREATE TABLE IF NOT EXISTS find_valuation(
    id            INT           PRIMARY KEY,
    channel       VARCHAR(50)   NOT NULL COMMENT '收到处理消息的频道',
    fogname       VARCHAR(100)  NOT NULL COMMENT '文件唯一标识',
    storage_type  VARCHAR(50)   NOT NULL COMMENT '存储器',
    storage_point VARCHAR(100)  NOT NULL COMMENT '存储位置',
    is_valuation  TINYINT       NOT NULL COMMENT '是否为估值表文件' # 0 => 否; 1 => 是; -1 => 检查程序出问题没有给出结果
);


