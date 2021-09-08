# coding=utf-8

from X2.XMessage.xmail.connect import SMTPBox

if __name__ == '__main__':

    hostname = ''
    username = ''
    password = ''

    send_subject = ''
    send_message = ''
    recipients = []
    cc = []

    # ==============================================================================
    # connection
    box = SMTPBox(host=hostname,
                  username=username,
                  password=password)

    # ==============================================================================
    # send message
    box.send(subject=send_subject,
             recipients=recipients,
             cc=cc,
             text=send_message)

