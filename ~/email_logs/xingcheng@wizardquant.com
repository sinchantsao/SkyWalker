2021-08-30 10:40:59 - MainThread - INFO - X2.XMessage.xmail - Created IMAP4 transport for imap.exmail.qq.com:993
2021-08-30 10:41:00 - MainThread - INFO - X2.XMessage.xmail - Logged into server imap.exmail.qq.com and selected mailbox 'INBOX'
2021-08-30 10:41:00 - MainThread - INFO - X2.XMessage.xmail - Connected to IMAP Server with user xingcheng@wizardquant.com on imap.exmail.qq.com over SSL
2021-08-30 10:41:00 - MainThread - INFO - X2.XMessage.xmail - Created IMAP4 transport for imap.exmail.qq.com:993
2021-08-30 10:41:00 - MainThread - INFO - X2.XMessage.xmail - Logged into server imap.exmail.qq.com and selected mailbox 'INBOX'
2021-08-30 10:41:00 - MainThread - INFO - X2.XMessage.xmail - Connected to IMAP Server with user xingcheng@wizardquant.com on imap.exmail.qq.com over SSL
2021-08-30 10:41:01 - MainThread - INFO - X2.XMessage.xmail - Created IMAP4 transport for imap.exmail.qq.com:993
2021-08-30 10:41:01 - MainThread - INFO - X2.XMessage.xmail - Logged into server imap.exmail.qq.com and selected mailbox 'INBOX'
2021-08-30 10:41:01 - MainThread - INFO - X2.XMessage.xmail - Connected to IMAP Server with user xingcheng@wizardquant.com on imap.exmail.qq.com over SSL
2021-08-30 10:41:01 - MainThread - INFO - X2.XMessage.xmail - Created IMAP4 transport for imap.exmail.qq.com:993
2021-08-30 10:41:02 - MainThread - INFO - X2.XMessage.xmail - Logged into server imap.exmail.qq.com and selected mailbox 'INBOX'
2021-08-30 10:41:02 - MainThread - INFO - X2.XMessage.xmail - Connected to IMAP Server with user xingcheng@wizardquant.com on imap.exmail.qq.com over SSL
2021-08-30 10:41:02 - MainThread - INFO - X2.XMessage.xmail - Created IMAP4 transport for imap.exmail.qq.com:993
2021-08-30 10:41:02 - MainThread - INFO - X2.XMessage.xmail - Logged into server imap.exmail.qq.com and selected mailbox 'INBOX'
2021-08-30 10:41:02 - MainThread - INFO - X2.XMessage.xmail - Connected to IMAP Server with user xingcheng@wizardquant.com on imap.exmail.qq.com over SSL
2021-08-30 10:41:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:41:02 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:41:02 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:41:02 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:41:02 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:41:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:41:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 113; Online number of UID is 97; Diff number of UID is 7
2021-08-30 10:41:02 -   Thread-1 - INFO - X2.XMessage.xmail - Query mail content from folder TGSeries by UID 411
2021-08-30 10:41:02 -   Thread-2 - INFO - X2.XMessage.xmail - Query mail content from folder TGSeries by UID 412
2021-08-30 10:41:02 -   Thread-3 - INFO - X2.XMessage.xmail - Query mail content from folder TGSeries by UID 413
2021-08-30 10:41:02 -   Thread-4 - INFO - X2.XMessage.xmail - Query mail content from folder TGSeries by UID 414
2021-08-30 10:41:25 -   Thread-1 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_411.context' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:25 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_412.context' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:25 -   Thread-1 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_411_641ec.txt' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:25 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_412_28b25.txt' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:25 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_412_b33a9.txt' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:25 -   Thread-2 - INFO - X2.XMessage.xmail - Query mail content from folder TGSeries by UID 415
2021-08-30 10:41:25 -   Thread-1 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_411_e3e67.txt' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:25 -   Thread-1 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_411_6bb78.txt' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:26 -   Thread-1 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_411_98119.txt' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:26 -   Thread-4 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_414.context' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:26 -   Thread-1 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_411_296b0.txt' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:26 -   Thread-3 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_413.context' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:26 -   Thread-4 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_414_740b8.xls' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:26 -   Thread-1 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_411_62de8.txt' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:26 -   Thread-3 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_413_c24dd.xls' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:26 -   Thread-4 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_414_97a3b.xls' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:27 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_415.context' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:27 -   Thread-1 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_411_8daaa.txt' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:27 -   Thread-3 - INFO - X2.XMessage.xmail - Query mail content from folder TGSeries by UID 416
2021-08-30 10:41:27 -   Thread-4 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_414_991c0.xls' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:27 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_415_f1805.xls' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:27 -   Thread-1 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_411_29f44.txt' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:27 -   Thread-4 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_414_4d6e6.xls' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:27 -   Thread-2 - INFO - X2.XMessage.xmail - Query mail content from folder TGSeries by UID 417
2021-08-30 10:41:27 -   Thread-4 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_414_e91db.xls' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:27 -   Thread-1 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_411_00e2d.txt' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:27 -   Thread-4 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_414_3602b.xls' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:27 -   Thread-4 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_414_b697d.xlsx' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:28 -   Thread-4 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_414_87eca.xls' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:28 -   Thread-1 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_411_0891d.txt' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:28 -   Thread-4 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_414_2a146.xls' to EmailFile[bucket] xingcheng/20210827/[namespace]
2021-08-30 10:41:29 -   Thread-3 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_416.context' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:29 -   Thread-3 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_416_149d1.xls' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:48 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_417.context' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:48 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_417_004bf.txt' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:49 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_417_1ec17.txt' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:49 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_417_d9e4b.txt' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:50 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_417_3e35c.txt' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:50 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_417_d3ec0.txt' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:50 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_417_4877f.txt' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:51 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_417_59f6f.txt' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:53 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_417_3b796.txt' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:41:54 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_417_33c10.txt' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:42:00 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_417_942e1.txt' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:42:29 -   Thread-2 - INFO - X2.XMessage.xmail - Write mail context 'xingcheng_TGSeries_417_d3802.txt' to EmailFile[bucket] xingcheng/20210830/[namespace]
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:43:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:45:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:45:02 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:45:02 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:45:02 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:45:02 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:45:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:45:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:45:02 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:45:02 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:45:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:45:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:45:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:45:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:45:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:47:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:49:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:51:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:53:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:53:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:53:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:53:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:53:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:53:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:53:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:53:03 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:53:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:53:03 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:53:03 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:53:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:53:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:53:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:55:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:57:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 10:59:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:01:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:03:04 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:03:04 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:03:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:03:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:03:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:03:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:03:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:03:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:03:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:03:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:03:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:03:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:03:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:03:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:05:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:07:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:09:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:11:05 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:11:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:11:05 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:11:05 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:11:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:11:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:11:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:11:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:11:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:11:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:11:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:11:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:11:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:11:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:13:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:15:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:17:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:19:06 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:19:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:19:06 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:19:06 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:19:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:19:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:19:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:19:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:19:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:19:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:19:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:19:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:19:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:19:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:21:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:23:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:25:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:27:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:27:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:27:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:27:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:27:07 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:27:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:27:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:27:07 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:27:07 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:27:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:27:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:27:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:27:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:27:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:29:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:31:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:33:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:35:08 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:35:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:35:08 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:35:08 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:35:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:35:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:35:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:35:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:35:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:35:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:35:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:35:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:35:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:35:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:37:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:39:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:41:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:43:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:43:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:43:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:43:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:43:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:43:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:43:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:43:09 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:43:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:43:09 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:43:09 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:43:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:43:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:43:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:45:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:47:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:49:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:51:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:53:10 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:53:10 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:53:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:53:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:53:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:53:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:53:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:53:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:53:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:53:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:53:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:53:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:53:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:53:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:55:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:57:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 11:59:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:01:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:01:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:01:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:01:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:01:11 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:01:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:01:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:01:11 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:01:11 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:01:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:01:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:01:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:01:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:01:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:03:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:05:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:07:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:09:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:11:12 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:11:12 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:11:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:11:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:11:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:11:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:11:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:11:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:11:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:11:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:11:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:11:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:11:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:11:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:13:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:15:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:17:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:19:13 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:19:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:19:13 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:19:13 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:19:14 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:19:14 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:19:14 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:19:14 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:19:14 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:19:14 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:19:14 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:19:14 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:19:14 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:19:14 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Wanna query UID from folder TGSeries by index from 1 to inf.
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 1 to 100001.
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail - Get UID from 321 to 417, total 97 uid numbers.
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail - Query UID info from folder TGSeries by indexes from 100002 to 200002.
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail - Get nothing about uid.
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Actually get mail uid info from 321 to 417 from TGSeries, total 97
2021-08-30 12:21:14 -   Thread-5 - INFO - X2.XMessage.xmail.auto - Folder => TGSeries: Local number of UID is 120; Online number of UID is 97; Diff number of UID is 0
