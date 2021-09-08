# coding=utf8
__author__ = 'caoxingcheng'

from WQCommon.hipchat import sendRoomNotification as _send_room_notification

_DEFAULT_ROOM_NUMBER = '983'
test_msg = """
<html>
  <strong>
    hello dev.
    there is X2 toolkit message room.
  </strong>
</html>
"""


def set_room(room):
    global _DEFAULT_ROOM_NUMBER
    _MSG_ROOM_NUMBER = room


def test_send_msg():
    send_or_not = _send_room_notification(room_id_or_name=_DEFAULT_ROOM_NUMBER,
                                          message=test_msg,
                                          message_format='html')
    if send_or_not:
        print('test success!')
    else:
        print('test error!')


def send_error(msg):
    _send_room_notification(room_id_or_name=_DEFAULT_ROOM_NUMBER,
                            message=msg,
                            color='red')


def send_notify(msg):
    return _send_room_notification(room_id_or_name=_DEFAULT_ROOM_NUMBER,
                                   message=msg,
                                   color='yellow')


def send_msg(msg):
    return _send_room_notification(room_id_or_name=_DEFAULT_ROOM_NUMBER,
                                   message=msg,
                                   color='green')
