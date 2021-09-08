# coding=utf8

import os
from threading import local
try:
    from AvengerPy import AvengerAccessor
except ImportError:
    from AvengerPyRO import AvengerAccessor
from X1.stand import ParamStandError


__avenger_username = "AVENGER_USERNAME"
__avenger_password = "AVENGER_PASSWORD"

Connections = local()

def get_default_client():
    client = getattr(Connections, "avenger_client", None)
    if client is None:
        try:
            username = os.environ[__avenger_username]
            password = os.environ[__avenger_password]
        except KeyError:
            raise ParamStandError(
                "You're using default client, but can not found environment variable about "
                f"`{__avenger_username}` and `{__avenger_password}`."
            )
        client = AvengerAccessor()
        client.login(username, password)
        setattr(Connections, "avenger_client", client)
    return client


def join_avenger_location(source, file_id):
    return ':'.join((source, file_id))


def split_avenger_location(location):
    source, file_id = location.split(':', 1)
    return source, file_id

