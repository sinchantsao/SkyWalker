#### 环境变量
  - `X2.XDB.sql.connections.LocalStorage` (SQLite DB)默认位置 `$HOME/X2_SQLite_DB.db`
  - `X2.XMessage.xmail.record.RecordsStorage`(SQLite DB)邮件下载记录存储默认位置 `$HOME/.mail_metadata.db`

  - 以下配置用于CEPH分布式存储使用
    - `CEPH_ENDPOINT`(使用CEPH存储时该参必须给定)
    - 以下二选一
      - access key参数直连方式(该形式优先,可以尽可能避免错误)
        - `CEPH_ACCESS_KEY`
        - `CEPH_ACCESS_SEC`
      - LDAP形式
        - `LDAP_USERNAME`
        - `LDAP_PASSWORD`

  - 配置了以下参数，在下载邮件的时候 MySQL 将会记录下载邮件信息，否则仅在本地使用 SQLite 记录
    - `X2_MAIL_MYSQL_USER`
    - `X2_MAIL_MYSQL_PASSWORD`
    - `X2_MAIL_MYSQL_DB`
    - `X2_MAIL_MYSQL_HOST`
    - `X2_MAIL_MYSQL_PORT`

  - 需要Avenger连接时，需要配置以下参数
    - `AVENGER_USERNAME`
    - `AVENGER_PASSWORD`

  - 需要更新本地股票基本数据时需要配置tushare的token信息
    - `TUSHARE_TOKEN`