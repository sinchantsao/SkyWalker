# coding=utf8

import base64
import boto3
import logging
import os
import threading
import typing as t
from botocore.config import Config
from X1.stand import ParamStandError, ArgStandError

_logger = logging.getLogger(__name__)

__ceph_access_key = "CEPH_ACCESS_KEY"
__ceph_access_sec = "CEPH_ACCESS_SEC"
__ceph_endpoint = "CEPH_ENDPOINT"
__ldap_username = "LDAP_USERNAME"
__ldap_password = "LDAP_PASSWORD"

_ThreadLocal = threading.local()
_no_ldap_env = "You are using default configs, please check out the three " \
               f"`{__ceph_endpoint}` & `{__ldap_username}` & `{__ldap_password}` " \
               f"in os environment variables. " \
               f"Otherwise params of `{__ceph_endpoint}` & `{__ceph_access_key}` & `{__ceph_access_sec}`."


def gen_ceph_keys(username, password):
    token = """{{
        "RGW_TOKEN": {{
            "version": 1,
            "type": "ldap",
            "id": "{}",
            "key": "{}"
        }}   
    }}""".format(username, password)
    token_bytes = str(token).encode("utf-8")  # ascii
    return base64.b64encode(token_bytes).decode("utf-8")


def login_ceph(username: str = None, password: str = None,
               endpoint_url: str = "http://ceph.wq",
               access_key: str = None, access_sec: str = None):
    """
    登陆 S3类 server 获取连接,
    username 和 password 为 LDAP 服务账户名密码.
    access_key 和 access_sec 为直连验证信息, 需要与 ceph 管理员联系获取.
    Args:
        username: LDAP 服务账户名
        password: LDAP 服务密码
        endpoint_url: ceph 服务地址
        access_key: 直连验证 key 信息, 与 ceph 管理员联系获取.
        access_sec: 直连验证 secret 信息, 与 ceph 管理员联系获取

    Returns: S3 服务连接对象.
    """
    # # login by ldap
    # aws_access_key_id = gen_ceph_keys(username, password)
    # aws_access_key_id = ""
    # aws_secret_access_key = ""

    # # skip ldap by secret directly
    # aws_access_key_id = "T6JJH9VW5644C7N2BTTF"
    # aws_secret_access_key = "FD764ofyGrLD7P7EsDeF7JmJeXIasgLV8jSadh1k"

    if access_key and access_sec:
        aws_access_key_id = access_key
        aws_secret_access_key = access_sec
    elif username is None or password is None:
        raise ArgStandError(
            "You did not pass access key and access secret, "
            "so you have to refer username and password."
        )
    else:
        aws_access_key_id = gen_ceph_keys(username, password)
        aws_secret_access_key = ""

    config = Config(connect_timeout=600, read_timeout=600, signature_version="s3")
    s3 = boto3.resource(
        "s3",  # service name
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=config
    )
    _logger.debug(f"New connection to ceph endpoint {endpoint_url} with {username}")
    return s3


def get_default_boto3sev():
    """
    根据环境变量获取 ceph 连接, 优先通过直连验证信息获取连接.
      - 直连
        - `CEPH_ACCESS_KEY`
        - `CEPH_ACCESS_SEC`
      - LDAP形式
        - `LDAP_USERNAME`
        - `LDAP_PASSWORD`
    """
    boto3sev = getattr(_ThreadLocal, "ceph_conn", None)

    if boto3sev is None:
        endpoint = os.environ.get(__ceph_endpoint, None)
        if endpoint is None:
            raise ParamStandError(_no_ldap_env)

        access_key = os.environ.get(__ceph_access_key, None)
        access_sec = os.environ.get(__ceph_access_sec, None)
        if access_key and access_sec:
            boto3sev = login_ceph(None, None, endpoint, access_key=access_key, access_sec=access_sec)
            _logger.debug("Login into ceph by access key and access secret directly.")
        else:
            try:
                username = os.environ[__ldap_username]
                password = os.environ[__ldap_password]
            except KeyError:
                raise ParamStandError(_no_ldap_env)
            boto3sev = login_ceph(username, password, endpoint)
        setattr(_ThreadLocal, "ceph_conn", boto3sev)
    return boto3sev


def ceph_upload(bytesflow, bucket: str, prefix: str, fid: str, conn):
    """

    Args:
        bytesflow: 文件字节流对象.
        bucket: s3 概念, 桶.
        prefix: 与 fid 组成唯一标识符 key(s3概念)--可以按照 Unix 文件绝对路径来理解,
                prefix 为文件目录路径, 与 fid 文件名组成文件绝对路径.
        fid: ... .
        conn: ceph 连接对象.

    Returns:

    """
    key = format_prefix(prefix) + fid
    response = conn.Object(bucket_name=bucket, key=key).put(Body=bytesflow)
    return response


def ceph_download(bucket: str, prefix: str, fid: str, conn) -> bytes:
    key = format_prefix(prefix) + fid
    response = conn.Object(bucket_name=bucket, key=key).get()
    buff = response["Body"]
    bytesflow = buff.read()
    return bytesflow


def join_ceph_location(bucket, prefix):
    """
    当文件需要存储到 ceph 分布式数据库时, 如果需要对其记录,
    采用 SQL 表记录, bucket 和文件路径(prefix) 将拼接作为 SQL 表中 storage_point 字段数据存储.
    Args:
        bucket: s3概念
        prefix: 文件分类路径

    Returns: storage_point
    """
    return ':'.join((bucket, prefix))


def split_ceph_location(location) -> t.Tuple[str, str]:
    """
    存储在结构化数据库中的记录表存在字段 storage_point 字段,
    其表明了数据存储在 ceph 中的 bucket 和路径 key(与实际 key 不同(路径只为分类文件),
    想要得到实际 key 还需 prefix 与 fogname 字段 进行路径拼接).

    storage_point 样例: BucketName: this/is/prefix/path .
    实际 key 拼接样例: os.path.join(prefix, fogname) .

    Returns: bucket: str, prefix: str

    """
    bucket, prefix = location.split(':', 1)
    return bucket, prefix


def format_prefix(prefix: str) -> str:
    return prefix.strip('/') + '/'
