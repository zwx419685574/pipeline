# coding=utf8
import json

from flask import Flask, render_template, jsonify, redirect
from chatroom import send_onegroup, group
import itchat
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

LOGINSTATUS = False


@app.route('/')
def hello_world():
    return 'cc'


@app.route('/getchatroom')
def get_chatroom():
    groups = itchat.get_chatrooms(update=True)
    print '群数量有 %s个' % len(groups)
    return jsonify(groups)


@app.route('/wechat/<msg>')
def wechat(msg):
    gname = group()
    send_onegroup(msg, gname)
    return 'send msg ok'


def back(uuid, status, qrcode):
    with open(r'QR.png', 'wb') as f:
        f.write(qrcode)


def login_back():
    LOGINSTATUS = True
    pass


@app.route('/login')
def login():
    # itchat.logout()
    itchat.auto_login(hotReload=True,picDir=r'QR.png',qrCallback=back,loginCallback=login_back)
    if LOGINSTATUS:
        # 162上端口为 8090
        return redirect('http://127.0.0.1:8090/flask_wechat_front/')
    else:
        return False


@app.route('/friends')
def get_friends():
    friends = itchat.get_friends()
    print 'your friends num is %s' % len(friends)
    # return json.dumps(friends)
    return jsonify(friends)
    # return 'get friends ok, num is %s' % len(friends)


@app.route('/searchfriend/<name>')
def search_friend(name):
    info = itchat.search_friends(nickName=name)[0]
    return jsonify(info)


@app.route('/msgtofriend/<fname>/<msg>')
def send_msg_to_friend(fname,msg):
    name = itchat.search_friends(name=fname)
    realname = name[0]["UserName"]
    itchat.send(msg, realname)
    return 'send friend msg ok'


@app.route('/logout')
def logout():
    itchat.logout()
    return redirect('http://127.0.0.1:8090/flask_wechat_front/')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
