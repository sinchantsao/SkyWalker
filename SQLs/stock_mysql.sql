# version < MySQL 8.0.19

SET @trade_account_eng = 'trade account',
    @trade_account_cn  = '交易账号',

    @trade_date_eng = 'trade date',
    @trade_date_cn = '交易日期',

    @total_asset_eng = 'total asset',
    @total_asset_cn  = '总资产',

    @netvalue_eng = 'netvalue',
    @netvalue_cn  = '净资产',

    @total_marketvalue_eng = 'total marketvalue',
    @total_marketvalue_cn  = '总市值',

    @fund_balance_eng = 'fund balance',
    @fund_balance_cn  = '资金余额',

    @total_liabilities_eng = 'total liabilities',
    @total_liabilities_cn  = '总负债',

    @bonds_liabilities_eng = 'bonds liabilities',
    @bonds_liabilities_cn  = '融券负债',

    @financed_liabilities_eng = 'financed liabilities',
    @financed_liabilities_cn  = '融资负债',

    @stock_position_eng = 'stock position',
    @stock_position_cn  = '股票持仓',

    @trade_flow_eng = 'trade flow',
    @trade_flow_cn  = '交易流水',

    @contract_position_eng = 'contract position',
    @contract_position_cn  = '合约持仓';


# ---------------------------------------------------------------------------------
# 股票市场基本信息
# ---------------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS stock_market_info;
USE stock_market_info;

CREATE TABLE IF NOT EXISTS `stock_base_info`(
    stock_code VARCHAR(15) PRIMARY KEY COMMENT '股票代码',
    stock_name VARCHAR(50) NOT NULL COMMENT '股票名称',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;

# ---------------------------------------------------------------------------------
# 股票交易信息解析器管理库
# ---------------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS `stock_parse`;
USE `stock_parse`;

# 支持文件类型管理(独立
CREATE TABLE IF NOT EXISTS `parse_file_types`(
    id          INT         AUTO_INCREMENT UNIQUE,
    extension   VARCHAR(30) NOT NULL COMMENT '文件后缀',
    file_type   VARCHAR(30) NOT NULL COMMENT '文件类型',
    PRIMARY KEY(id, extension, file_type)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;
INSERT INTO `parse_file_types`(id, extension, file_type)
VALUES (1, 'xls',  'excel'),
       (2, 'XLS',  'excel'),
       (3, 'xlsx', 'excel'),
       (4, 'XLSX', 'excel'),
       (5, 'txt',  'txt'),
       (6, 'TXT',  'txt'),
       (7, 'csv',  'csv'),
       (8, 'CSV',  'csv'),
       (8, 'pdf',  'pdf'),
       (8, 'PDF',  'pdf')
ON DUPLICATE KEY UPDATE
    id=VALUES(id),
    extension=VALUES(extension),
    file_type=VALUES(file_type);

# 券商信息(独立
CREATE TABLE IF NOT EXISTS securities_info(
    id   MEDIUMINT       PRIMARY KEY AUTO_INCREMENT,
    name_cn     VARCHAR(100)    NOT NULL    COMMENT '券商名称',
    name_eng    VARCHAR(50)     NOT NULL    COMMENT '英文名',
    name_short  VARCHAR(20)     NOT NULL    COMMENT '英文简称'
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;
# https://jg.sac.net.cn/pages/publicity/securities-list.html
# 如果新增券商不建议修改对应id进行增加,而是在脚本基础上自增编号;
# 尽可能不改变原有编号,迁移可能导致原有数据错误;
# 若果是从0部署可以自行修改;
INSERT INTO securities_info(id, name_cn, name_eng, name_short)
VALUES (1, '未指定券商', 'No Specified', 'No Specified'),
       (2, '爱建证券有限责任公司', 'AJZQ', 'AJZQ'),
       (3, '安信证券股份有限公司', 'ESSENCE', 'ESSENCE'),
       (4, '安信证券资产管理有限公司', 'AXZQZG', 'AXZQZG'),
       (5, '北京高华证券有限责任公司', 'GHSL', 'GHSL'),
       (6, '渤海汇金证券资产管理有限公司', 'Bohai Huijin Securities Asset Management CO.,LTD', 'BHHJZG'),
       (7, '渤海证券股份有限公司', 'Bohai Securities', 'BHZQ'),
       (8, '财达证券股份有限公司', 'Caida Securities', 'CDZQ'),
       (9, '财通证券股份有限公司', 'Caitong Securities', 'CTSEC'),
       (10, '财通证券资产管理有限公司', 'Caitong Securities Asset Management CO.,LTD', 'CTZG'),
       (11, '财信证券有限责任公司', 'Chasing Securities', 'CFZQ'),
       (12, '长城国瑞证券有限公司', 'Great Wall Glory Securities', 'GWGSC'),
       (13, '长城证券股份有限公司', '', ''),
       (14, '长江证券（上海）资产管理有限公司', '', ''),
       (15, '长江证券承销保荐有限公司', '', ''),
       (16, '长江证券股份有限公司', '', ''),
       (17, '川财证券有限责任公司', '', ''),
       (18, '大通证券股份有限公司', '', ''),
       (19, '大同证券有限责任公司', '', ''),
       (20, '德邦证券股份有限公司', '', ''),
       (21, '德邦证券资产管理有限公司', '', ''),
       (22, '第一创业证券承销保荐有限责任公司', '', ''),
       (23, '第一创业证券股份有限公司', '', ''),
       (24, '东北证券股份有限公司', '', ''),
       (25, '东方财富证券股份有限公司', '', ''),
       (26, '东方证券承销保荐有限公司', '', ''),
       (27, '东方证券股份有限公司', '', ''),
       (28, '东海证券股份有限公司', '', ''),
       (29, '东吴证券股份有限公司', '', ''),
       (30, '东兴证券股份有限公司', '', ''),
       (31, '东亚前海证券有限责任公司', '', ''),
       (32, '东证融汇证券资产管理有限公司', '', ''),
       (33, '东莞证券股份有限公司', '', ''),
       (34, '方正证券承销保荐有限责任公司', '', ''),
       (35, '方正证券股份有限公司', '', ''),
       (36, '高盛高华证券有限责任公司', '', ''),
       (37, '光大证券股份有限公司', '', ''),
       (38, '广发证券股份有限公司', '', ''),
       (39, '广发证券资产管理（广东）有限公司', '', ''),
       (40, '国都证券股份有限公司', '', ''),
       (41, '国海证券股份有限公司', '', ''),
       (42, '国金证券股份有限公司', '', ''),
       (43, '国开证券股份有限公司', '', ''),
       (44, '国联证券股份有限公司', '', ''),
       (45, '国融证券股份有限公司', '', ''),
       (46, '国盛证券有限责任公司', '', ''),
       (47, '国盛证券资产管理有限公司', '', ''),
       (48, '国泰君安证券股份有限公司', '', ''),
       (49, '国信证券股份有限公司', '', ''),
       (50, '国元证券股份有限公司', '', ''),
       (51, '海通证券股份有限公司', '', ''),
       (52, '恒泰长财证券有限责任公司', '', ''),
       (53, '恒泰证券股份有限公司', '', ''),
       (54, '宏信证券有限责任公司', '', ''),
       (55, '红塔证券股份有限公司', '', ''),
       (56, '华安证券股份有限公司', '', ''),
       (57, '华宝证券股份有限公司', '', ''),
       (58, '华创证券有限责任公司', '', ''),
       (59, '华福证券有限责任公司', '', ''),
       (60, '华金证券股份有限公司', '', ''),
       (61, '华林证券股份有限公司', '', ''),
       (62, '华龙证券股份有限公司', '', ''),
       (63, '华融证券股份有限公司', '', ''),
       (64, '华泰联合证券有限责任公司', '', ''),
       (65, '华泰证券（上海）资产管理有限公司', '', ''),
       (66, '华泰证券股份有限公司', '', ''),
       (67, '华西证券股份有限公司', '', ''),
       (68, '华兴证券有限公司', '', ''),
       (69, '华英证券有限责任公司', '', ''),
       (70, '华鑫证券有限责任公司', '', ''),
       (71, '汇丰前海证券有限责任公司', '', ''),
       (72, '江海证券有限公司', '', ''),
       (73, '金通证券有限责任公司', '', ''),
       (74, '金元证券股份有限公司', '', ''),
       (75, '金圆统一证券有限公司', '', ''),
       (76, '九州证券股份有限公司', '', ''),
       (77, '开源证券股份有限公司', '', ''),
       (78, '联储证券有限责任公司', '', ''),
       (79, '民生证券股份有限公司', '', ''),
       (80, '摩根大通证券（中国）有限公司', '', ''),
       (81, '摩根士丹利华鑫证券有限责任公司', '', ''),
       (82, '南京证券股份有限公司', '', ''),
       (83, '平安证券股份有限公司', '', ''),
       (84, '瑞信方正证券有限责任公司', '', ''),
       (85, '瑞银证券有限责任公司', '', ''),
       (86, '山西证券股份有限公司', '', ''),
       (87, '上海东方证券资产管理有限公司', '', ''),
       (88, '上海光大证券资产管理有限公司', '', ''),
       (89, '上海国泰君安证券资产管理有限公司', '', ''),
       (90, '上海海通证券资产管理有限公司', '', ''),
       (91, '上海证券有限责任公司', '', ''),
       (92, '上海甬兴证券资产管理有限公司', '', ''),
       (93, '申港证券股份有限公司', '', ''),
       (94, '申万宏源西部证券有限公司', '', ''),
       (95, '申万宏源证券承销保荐有限责任公司', '', ''),
       (96, '申万宏源证券有限公司', '', ''),
       (97, '世纪证券有限责任公司', '', ''),
       (98, '首创证券股份有限公司', '', ''),
       (99, '太平洋证券股份有限公司', '', ''),
       (100, '天风（上海）证券资产管理有限公司', '', ''),
       (101, '天风证券股份有限公司', '', ''),
       (102, '万和证券股份有限公司', '', ''),
       (103, '万联证券股份有限公司', '', ''),
       (104, '网信证券有限责任公司', '', ''),
       (105, '五矿证券有限公司', '', ''),
       (106, '西部证券股份有限公司', '', ''),
       (107, '西南证券股份有限公司', '', ''),
       (108, '湘财证券股份有限公司', '', ''),
       (109, '新时代证券股份有限公司', '', ''),
       (110, '信达证券股份有限公司', '', ''),
       (111, '兴业证券股份有限公司', '', ''),
       (112, '兴证证券资产管理有限公司', '', ''),
       (113, '野村东方国际证券有限公司', '', ''),
       (114, '银河金汇证券资产管理有限公司', '', ''),
       (115, '银泰证券有限责任公司', '', ''),
       (116, '英大证券有限责任公司', '', ''),
       (117, '粤开证券股份有限公司', '', ''),
       (118, '招商证券股份有限公司', '', ''),
       (119, '招商证券资产管理有限公司', '', ''),
       (120, '浙江浙商证券资产管理有限公司', '', ''),
       (121, '浙商证券股份有限公司', '', ''),
       (122, '中德证券有限责任公司', '', ''),
       (123, '中国国际金融股份有限公司', '', ''),
       (124, '中国银河证券股份有限公司', '', ''),
       (125, '中国中金财富证券有限公司', '', ''),
       (126, '中航证券有限公司', '', ''),
       (127, '中山证券有限责任公司', '', ''),
       (128, '中泰证券（上海）资产管理有限公司', '', ''),
       (129, '中泰证券股份有限公司', '', ''),
       (130, '中天国富证券有限公司', '', ''),
       (131, '中天证券股份有限公司', '', ''),
       (132, '中信建投证券股份有限公司', '', ''),
       (133, '中信证券（山东）有限责任公司', '', ''),
       (134, '中信证券股份有限公司', '', ''),
       (135, '中信证券华南股份有限公司', '', ''),
       (136, '中银国际证券股份有限公司', '', ''),
       (137, '中邮证券有限责任公司', '', ''),
       (138, '中原证券股份有限公司', '', ''),
       (139, '甬兴证券有限公司', '', '')
ON DUPLICATE KEY UPDATE
    id=VALUES(id),
    name_cn=VALUES(name_cn),
    name_eng=VALUES(name_eng),
    name_short=VALUES(name_short);

# 解析数据归属类型(独立
# type:
#   1 => index
#   2 => table
CREATE TABLE IF NOT EXISTS `parsed_data_genus`(
    id          MEDIUMINT       PRIMARY KEY AUTO_INCREMENT,
    type        TINYINT         NOT NULL,
    name_cn     VARCHAR(100)    NOT NULL,
    name_eng    VARCHAR(50)     NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;
INSERT INTO `parsed_data_genus`(id, type, name_cn, name_eng)
VALUES (1, 1,  @trade_account_cn,          @trade_account_eng),
       (2, 1,  @trade_date_cn,             @trade_date_eng),
       (3, 1,  @total_asset_cn,            @total_asset_eng),
       (4, 1,  @netvalue_cn,               @netvalue_eng),
       (5, 1,  @total_marketvalue_cn,      @total_marketvalue_eng),
       (6, 1,  @fund_balance_cn,           @fund_balance_eng),
       (7, 1,  @total_liabilities_cn,      @total_liabilities_eng),
       (8, 1,  @bonds_liabilities_cn,      @bonds_liabilities_eng),
       (9, 1,  @financed_liabilities_cn,   @financed_liabilities_eng),
       (10, 2, @trade_flow_cn,             @trade_flow_eng),
       (11, 2, @stock_position_cn,         @stock_position_eng),
       (12, 2, @contract_position_cn,      @contract_position_eng)
ON DUPLICATE KEY UPDATE
    id=VALUES(id),
    type=VALUES(type),
    name_cn=VALUES(name_cn),
    name_eng=VALUES(name_eng);

/*
解析指标规则管理
对于每一个正则表达式，都应该采用命名组合;
在框架中将会通过特定命名来进行数据匹配获取，未能按照规范命名则无效;
namespaces:
    单一指标:
        trade_account        => 交易账户
        trade_date           => 交易日期
        total_asset          => 总资产
        netvalue             => 净资产
        total_marketvalue    => 总市值
        fund_balance         => 资金余额
        total_liabilities    => 总负债
        bonds_liabilities    => 融券负债
        financed_liabilities => 融资负债
    表行数据:
        股票持仓:
            stock_code   => 股票代码
            stock_name   => 股票名称
            marketvalue  => 市值(单价
            marketprice  => 市价(单价
            pnl          => 收益
            amount       => 持仓数
        交易流水:
            trade_date     => 发生日期/交易日期
            event          => 摘要/交易事件
            stock_code     => 证券代码
            stock_name     => 证券名称
            volume         => 成交股数
            price          => 成交价格(单价
            quantities     => 发生金额
            balance        => 资金余额
            brokerage_fee  => 佣金
            transfer_fee   => 过户费
            service_charge => 手续费
            stamp_tax      => 印花税
            remarks        => 备注
        合约持仓:
            contract_date => 合约日期
            stock_code    => 证券代码
            stock_name    => 证券名称
            contract_type => 合约类型
            fund_paying   => 未了结合约金额
            fee_paying    => 未了结合约费用
            amount        => 未了结合约数量
            paying        => 未了结费用
            return_date   => 归还截止日
*/
CREATE TABLE IF NOT EXISTS txt_match_rules(
    id              INT             PRIMARY KEY     AUTO_INCREMENT,
    tag             VARCHAR(10)     DEFAULT ''      COMMENT '用户自定义标签',
    data_genus_id   MEDIUMINT       NOT NULL        COMMENT '解析归属类型:账号/总资产/净资产/持仓/流水/合约',
    brokerage_id    MEDIUMINT       DEFAULT 1       COMMENT '券商关联',

    data_regex      VARCHAR(1000)   NOT NULL        COMMENT '水平取值正则',
    check_regex     VARCHAR(1000)   DEFAULT NULL    COMMENT '`数据发现`正则',     # 用于触发取值正则
    check_follow    TINYINT         DEFAULT NULL    COMMENT '数据发现是否跟进',   # 触发取值时是否取值当前行数据
    uncheck_regex   VARCHAR(1000)   DEFAULT NULL    COMMENT '`数据结束`正则',     # 用于触发取消取值正则
    uncheck_follow  TINYINT         DEFAULT NULL    COMMENT '数据结束是否跟进',   # 触发取消取值时是否取值当前行数据

    vertical_by     VARCHAR(1000)   DEFAULT NULL    COMMENT '垂直取值关键词',
    vertical_space  TINYINT         DEFAULT NULL    COMMENT '垂直取值之间的行间隔',
    max_checkline   MEDIUMINT       DEFAULT NULL    COMMENT '发现数据痕迹起最多检索行数限制',
    active_lineno   INT             DEFAULT NULL    COMMENT '指定作用解析的行数',
    must_return     TINYINT         DEFAULT NULL    COMMENT '一定要有结果与否 NULL/TINYINT',
    priority        MEDIUMINT       DEFAULT 1       COMMENT '优先使用处理权级',
    delimit_sign    VARCHAR(10)     DEFAULT NULL    COMMENT '格式化文本数据分隔符',
    FOREIGN KEY (data_genus_id)     REFERENCES parsed_data_genus(id),
    FOREIGN KEY (brokerage_id)      REFERENCES securities_info(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

# 插入前检查,制定规范/规则‽
DELIMITER $$
CREATE TRIGGER txt_match_rules_strategy_check
BEFORE INSERT ON txt_match_rules
FOR EACH ROW
BEGIN
    # 如果指明vertical_by关键词,表明通过垂直形式获取数据;
    # 垂直形式获取数据仅用于单一指标数据的获取;
    # 垂直形式获取数据,必须指定数据与垂直关键词的行距;
    IF (vertical_by IS NOT NULL) AND (vertical_space IS NULL)
    THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'must specify vertical space if vertical key was set';
    END IF;
end
$$
DELIMITER ;

CREATE TABLE IF NOT EXISTS dataframe_indies_rules(
    id                      INT             PRIMARY KEY     AUTO_INCREMENT,
    tag                     VARCHAR(10)     DEFAULT ''      COMMENT '用户自定义标签',
    data_genus_id           MEDIUMINT       NOT NULL        COMMENT '解析归属类型:账号/总资产/净资产...',
    security_id             MEDIUMINT       DEFAULT 0       COMMENT '券商关联',
    front_wrap              VARCHAR(200)    DEFAULT NULL    COMMENT '正前cell关键词',
    header_wrap             VARCHAR(200)    DEFAULT NULL    COMMENT '正上cell关键词',
    # concat keywords by sign ‽
    header_kws              VARCHAR(5000)   DEFAULT NULL    COMMENT '',
    pick_space              TINYINT         DEFAULT NULL    COMMENT '正前/正上cell与数据之间的间隔距离',
    # origin1<=>map1;origin2<=>map2;origin3<=>map3...;
    header_maps             VARCHAR(5000)   DEFAULT NULL    COMMENT '',
    active_lineno           INT             DEFAULT NULL    COMMENT '指定作用解析的行数',
    must_return             TINYINT         DEFAULT 0       COMMENT '一定要有结果与否0/1',
    data_regex              TEXT            NOT NULL        COMMENT '被解析数据对应正则',
    # excel/csv => dataframe ‽
    start_lineno            INT         DEFAULT NULL    COMMENT '',
    FOREIGN KEY (data_genus_id) REFERENCES parsed_data_genus(id),
    FOREIGN KEY (security_id)  REFERENCES securities_info(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS table_fields(
    name_cn             VARCHAR(100) NOT NULL,
    name_eng            VARCHAR(100) NOT NULL,
    data_type           VARCHAR(10)  NOT NULL,
    refer_data_genus_id MEDIUMINT    NOT NULL,
    PRIMARY KEY (name_cn, refer_data_genus_id),
    FOREIGN KEY (refer_data_genus_id)
        REFERENCES parsed_data_genus (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;
INSERT INTO `table_fields`(name_cn, name_eng, data_type, refer_data_genus_id)
VALUES ('证券代码', 'stock code', 'str', 10),
       ('证券名称', 'stock name', 'str', 10),
       ('市价', 'marketprice', 'float', 10),
       ('市值', 'marketvalue', 'float', 10),
       ('盈亏', 'pnl', 'float', 10),
       ('股份余额', 'amount', 'float', 10),  # 不使用int是避免后续加入港股
       ('发生日期', 'trade date','str', 10),
       ('摘要', 'event', 'str', 10),
       ('成交股数', 'quantities', 'float', 10),
       ('成交价格', 'price', 'float', 10),
       ('发生金额', 'filled notional', 'float', 10),
       ('资金余额', 'balance', 'float', 10),
       ('佣金', 'brokerage fee', 'float', 10),
       ('过户费', 'transfer fee', 'float', 10),
       ('印花税', 'stamp duty', 'float', 10),

       ('证券代码', 'stock code', 'str', 11),
       ('证券名称', 'stock name', 'str', 11),
       ('持仓数', 'amount', 'float', 11),
       ('市值', 'marketvalue', 'float', 11),
       ('市价', 'marketprice', 'float', 11),
       ('收益', 'pnl', 'float', 11),

       ('合约日期', 'contract date', 'str', 12),
       ('证券代码', 'stock code', 'str', 12),
       ('证券名称', 'stock name', 'str', 12),
       ('合约类型', 'contract type', 'str', 12),
       ('未了结合约金额', 'fund paying', 'float', 12),
       ('未了结合约费用', 'fee paying', 'float', 12),
       ('未了结合约数量', 'amount', 'float', 12),
       ('未了结费用', 'paying', 'float', 12),
       ('归还截止日', 'return date', 'float', 12)
ON DUPLICATE KEY UPDATE
    name_cn=VALUES(name_cn),
    name_eng=VALUES(name_eng),
    data_type=VALUES(data_type),
    refer_data_genus_id=VALUES(refer_data_genus_id);


CREATE TABLE IF NOT EXISTS table_columns_maps(
    field_id   MEDIUMINT PRIMARY KEY AUTO_INCREMENT,
    field_name VARCHAR(100) NOT NULL,
    data_type  VARCHAR(10)  NOT NULL,
    map_name   VARCHAR(100) NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

