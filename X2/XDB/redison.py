# coding=utf8

import json
import os
import redis
import warnings
import typing as t
from threading import local
from uuid import uuid4
from X2.utlis import get_cur_microsecond
from X2.XMessage import _logger


PUBLIC_CHANNELS_KEY = "__PUB_CHANNELS__"
SUBSCRIBER_LISTS_KEY = "__SUBSCRIBER_LISTS__"


def convert_channel_name(channel):
    """ 频道注册到 redis 的名称 """
    return f"ch:{channel}"

def convert_subscriber_list_name(channel):
    """ 频道注册后启用的订阅者列表名称 """
    return f"subscriber-list:{channel}"

def convert_subscriber_channel_mq_name(channel, subscriber):
    """ 存储订阅用户对应频道发布数据的名称 """
    return ":".join((channel, subscriber))


class _RedisClient(redis.StrictRedis):
    """
    主要用来将 redis 作为消息件与之通信, 一个进程最好只有一个连接;
    连接在初始化过程中就做了线程隔离和限制, 不允许单个线程起多个连接,
    而进程内连接数控制由使用者控制, 还是同上建议, 一个进程内一个连接.

    建议根据 get_default_redis_client 函数配置对应环境变量获
    取连接.

    在模式上:

      - 为了消息防丢, 发布的数据将会被暂时存储.

      - 注册 channel 信息, 在 _PUBLIC_CHANNELS_KEY 全局变量
        对应的 KEY 中会设定 channel 名称信息, 这一数据为 redis
        中的 Hash 数据类型, 即 k-v 数据. 同时还会在 _SUBSCRIBER_LISTS_KEY
        全局变量对应的 KEY 中存储 channel 对应的订阅用户的 KEY
        信息, 同样为 Hash 数据类型.

      - 订阅 channel 信息, 会在 _SUBSCRIBER_LISTS_KEY 全局变
        量对应的 KEY 中确认该 channel 是否存在(在注册阶段就确保
        了该数据当中会有 channel 对应的订阅用户 KEY 信息); 获取
        到用户列表 KEY 信息后向其中添加当前连接信息(client_id),
        该数据为 redis 中的 Set 数据类型.

      - 发布信息, 根据给定的 channel 信息, 从 _PUBLIC_CHANNELS_KEY
        确认频道订阅者集合 KEY 从而得到订阅者信息, 向每一个订阅者
        特定的频道消息管理队列发送信息从而做到防丢, 并且向频道发送
        信息.

    """

    RedisConns = local()

    def __init__(self, host='localhost', port=6379,
                 db=0, password=None, socket_timeout=None,
                 socket_connect_timeout=None,
                 socket_keepalive=None, socket_keepalive_options=None,
                 connection_pool=None, unix_socket_path=None,
                 encoding='utf-8', encoding_errors='strict',
                 charset=None, errors=None,
                 decode_responses=False, retry_on_timeout=False,
                 ssl=False, ssl_keyfile=None, ssl_certfile=None,
                 ssl_cert_reqs='required', ssl_ca_certs=None,
                 ssl_check_hostname=False,
                 max_connections=None, single_connection_client=False,
                 health_check_interval=0, client_name=None, username=None,
                 # max_valid_msg=100,
                 keep_channel=False,
                 client_id=None, ):
        super(_RedisClient, self).__init__(host, port,
                                           db, password, socket_timeout,
                                           socket_connect_timeout,
                                           socket_keepalive, socket_keepalive_options,
                                           connection_pool, unix_socket_path,
                                           encoding, encoding_errors,
                                           charset, errors,
                                           decode_responses, retry_on_timeout,
                                           ssl, ssl_keyfile, ssl_certfile,
                                           ssl_cert_reqs, ssl_ca_certs,
                                           ssl_check_hostname,
                                           max_connections, single_connection_client,
                                           health_check_interval, client_name, username)
        conn = getattr(_RedisClient.RedisConns, "redis_conn", None)
        if conn is not None:
            raise RuntimeError("Only one redis connection is allowed for one thread.")

        # 如果由更复杂的场景应该考虑使用 GUID 替代
        self.client_id = client_id or uuid4().hex

        self._subscribed_channels = set()
        self._created_channels = set()

        self._keepchnanel = keep_channel

        # self.mq = deque(maxlen=max_valid_msg)

        self._listener = None

        setattr(_RedisClient.RedisConns, "redis_conn", self)
        _logger.debug(f"New connection to redis => {host}:{port}[{db}]"
                      f"{' with password ******' if password is not None else ''}.")

    def publish_json_message(self, channel, json_message):
        """
        从 __PUB_CHANNELS__ 中确认 channel 是否存在, 从 __SUBSCRIBER_LISTS__
        中获取 channel 相关订阅用户信息(client_id), 向每一个用户单独的有序序列中插
        入发布的相关数据,而有序序列 score 为时间戳(μs), member 则为发布的相关数据.

        Args:
            channel: 需要发布的 channel, 该 channel 必须是已经被注册的, 存在于
                     __PUB_CHANNELS__ 当中.
            json_message: 需要发布的 json 数据, 数据将会被序列化存储到中间件.

        """
        channel_name = self.hget(PUBLIC_CHANNELS_KEY, channel)
        if channel_name is None:
            raise ValueError(f"channel `{channel}` was not registered.")
        subscribe_list_name = self.hget(SUBSCRIBER_LISTS_KEY, channel)
        subscribers = self.smembers(subscribe_list_name)

        message = json.dumps(json_message)
        qmessage = {
            json.dumps(json_message): get_cur_microsecond()
        }
        for subscriber in subscribers:
            self.zadd(name=convert_subscriber_channel_mq_name(channel, subscriber),
                      mapping=qmessage)
        self.publish(channel_name, message)

    def __del__(self):
        for ch in self._subscribed_channels.copy():
            self.unsubscribe(ch)
        if not self._keepchnanel:
            for ch in self._created_channels.copy():
                self.unregister_channel(ch)
        super(_RedisClient, self).__del__()

    def subscribe(self, channel):
        """
        订阅一个 channel 必须保证这个 channel 存在,而在注册 channel 时,
        __PUB_CHANNELS__ / __SUBSCRIBER_LISTS__就存放了channel相关
        信息(参考方法 register_channel),只需要从中任意一个获取相关信息
        即可确认该channel是否存在;

        订阅时需要向相关订阅用户列表添加用户,因此这里采用从 __SUBSCRIBER_LISTS__
        中确认 channel 是否存在, 同时能取得订阅列表信息(key), 从而向订阅
        列表添加 client 信息.

        ==========================================================
        __SUBSCRIBER_LISTS__[channel] => {
            client_id(uniq),
            ...
        }

        Args:
            channel: 需要订阅信息的 channel

        """
        subscribe_list_name = self.hget(SUBSCRIBER_LISTS_KEY, channel)
        if subscribe_list_name is None:
            raise ValueError(f"channel `{channel}` was not registered.")
        if self._listener is None:
            self._listener = self.pubsub()
        self._listener.subscribe(channel)
        self.sadd(subscribe_list_name, self.client_id)
        self._subscribed_channels.add(channel)
        _logger.debug(f"Subscribe channel `{channel}`")

    def unsubscribe(self, channel):
        subscribe_list_name = self.hget(SUBSCRIBER_LISTS_KEY, channel)
        if subscribe_list_name is None:
            raise ValueError(f"channel `{channel}` was not registered.")
        if self._listener is None:
            raise RuntimeError("Make sure connection is listening before(subscribed?).")
        self._listener.unsubscribe(channel)
        result_1 = self.srem(subscribe_list_name, self.client_id)
        subscriber_mq = convert_subscriber_channel_mq_name(channel, self.client_id)
        result_2 = self.delete(subscriber_mq)
        self._subscribed_channels.remove(channel)
        _logger.debug(f"Unsubscribe channel,"
                      f"remove {self.client_id} from `{subscribe_list_name}` with return code {result_1}."
                      f"delete {subscriber_mq} with return code {result_2}.")

    def register_channel(self, channel):
        """
        用于注册 channel 信息, 在消息中间件当中会记录以下两项信息
          - channel 名称

            在消息中间件当中, 该名称用于 redis 订阅名称.
            channel 名称是在传入参数的基础上加上 `ch:` 前缀, 可以参考 convert_channel_name 函数的处理.
            在理解上传入的 channel 参数更类似于 topic, 用于指向起具体的 channel.

          - channel 订阅者存储 key

            在 redis 中注册一个 HASH 数据存储 Channel 名称信息
            PUB-CHANNELS => {
               channel: `$ch:channel`
               ...
            }

            在 redis 中注册一个 HASH 数据存储 channel 订阅者列表名称信息
            SUBSCRIBER-LISTS => {
                channel: `$subscriber-$list:channel`
                ...
            }
        """

        channel_name = convert_channel_name(channel)
        subscriber_listname = convert_subscriber_list_name(channel)

        name_returncode = self.hset(PUBLIC_CHANNELS_KEY, channel, f"{channel_name}")
        list_returncode = self.hset(SUBSCRIBER_LISTS_KEY, channel, f"{subscriber_listname}")
        self._created_channels.add(channel)
        _logger.debug(f"Register channel `{channel}`, "
                      f"set channel `{channel}` with name `{channel_name}` in {PUBLIC_CHANNELS_KEY} and return code is {name_returncode}, "
                      f"set channel `{channel}` subscriber list with name `{subscriber_listname}` in {SUBSCRIBER_LISTS_KEY} and return code is {list_returncode}.")

    def unregister_channel(self, channel):
        result_1 = self.hdel(PUBLIC_CHANNELS_KEY, channel)
        result_2 = self.hdel(SUBSCRIBER_LISTS_KEY, channel)
        self._created_channels.remove(channel)
        _logger.debug(f"Unregister channel `{channel}`, "
                      f"remove from {PUBLIC_CHANNELS_KEY} with return code {result_1}," 
                      f"remove from {SUBSCRIBER_LISTS_KEY} with return code {result_2}.")

    def listen(self):
        while True:
            yield next(self._listener.listen())

    def close(self):
        super(_RedisClient, self).close()
        del _RedisClient.RedisConns.redis_conn


Redis = _RedisClient

_default_redis_params_note = \
    "Process is creating default redis connection and could not find " \
    "{error_find_params} correctly in OS environments, " \
    "[X2_REDIS_HOST='{host}', X2_REDIS_PORT={port}, X2_REDIS_DB={db}] is going on."


def get_redis_client(**kwargs) -> _RedisClient:
    """
    根据环境变量或传入参数获取 Redis 连接

    环境变量:
        - X2_REDIS_HOST -> host
        - X2_REDIS_PORT -> port
        - X2_REDIS_DB -> db

    Args:
        kwargs:
          - host
          - port
          - db

    Returns: _RedisClient
    """

    conn = getattr(_RedisClient.RedisConns, "redis_conn", None)
    if conn is None:
        e = []
        params = {}
        pmaps = (("X2_REDIS_HOST", "X2_REDIS_PORT", "X2_REDIS_DB"),
                 ("host", "port", "db"))
        for k, m in zip(*pmaps):
            try:
                params[m] = os.environ[k]
            except KeyError:
                e.append(k)
        params.setdefault("host", "localhost")
        params.setdefault("port", 6639)
        params.setdefault("db", 0)
        if e:
            warnings.warn(
                _default_redis_params_note.format(
                    error_find_params="/".join(e),
                    **params)
            )
        params.update(kwargs)
        conn = _RedisClient(**params)
    return conn


