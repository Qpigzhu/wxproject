import random
import os,django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wxproject.settings")
django.setup()

from weixin.models import Wx

import itchat, time, sys

def output_info(msg):
    print('[INFO] %s' % msg)

def open_QR():
    while True:
        uuid = itchat.get_QRuuid()
        while uuid is None: uuid = itchat.get_QRuuid();time.sleep(1)
        code_img = itchat.get_QR(uuid)
        print(code_img)
        if code_img:
            # add_wx = Wx()
            # add_wx.code = 1
            # add_wx.code_img = code_img
            # add_wx.save()
            break
        time.sleep(1200)
    output_info('Please scan the QR Code')
    return uuid

uuid = open_QR()
waitForConfirm = False
while 1:
    status = itchat.check_login(uuid)
    if status == '200':
        break
    elif status == '201':
        if waitForConfirm:
            output_info('Please press confirm')
            waitForConfirm = True
    elif status == '408':
        output_info('Reloading QR Code')
        uuid = open_QR()
        waitForConfirm = False
userInfo = itchat.web_init()
itchat.show_mobile_login()
itchat.get_friends(True)
output_info('Login successfully as %s'%userInfo['NickName'])
itchat.start_receiving()

# Start auto-replying
@itchat.msg_register(itchat.content.NOTE)
def simple_reply(msg):
    if msg['Type'] == 'Text':
        return 'I received: %s' % msg['Content']
itchat.run()
