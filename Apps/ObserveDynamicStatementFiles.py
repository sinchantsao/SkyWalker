# coding=utf8

from queue import Queue as ThreadQueue
from X2.XDB.redison import get_redis_client

# 采用queue是为了创建进程有一个缓冲时间,避免消息过快而创建进程加载数据较多过慢,从而导错过了消息
loading_message = ThreadQueue()


# listen new file info
# 监听查看有没有新文件/邮件
def listen_new():
    redis = get_redis_client()
    while True:
        message = loading_message.get()


#   create process to spot
#   新建进程处理
def create_spot_process():
    pass


#       record file info
#       写入sql记录进程处理的文件信息:文件在哪里,叫什么


#       check out
#       判断处理


#       check out email info
#       邮箱信息符合吗
#       是否包含特定过滤信息


