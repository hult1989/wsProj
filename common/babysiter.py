# -*- coding:utf-8 -*-
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import Deferred, succeed, DeferredList
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.iweb import IBodyProducer
from zope.interface import implements
from twisted.internet.task import LoopingCall
from sendMail import sendMail
from json import dumps

import socket, sys, signal, os, time




server_address = ('localhost', 8081)
email_address = 'kindth@qq.com'

def testTcp():
    print 'TEST SOCKET!'
    tcplocation = '9,1024,ok'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    sock.sendall(tcplocation)
    data = sock.recv(96)
    if data != 'Result:9,1':
        raise Exception('server dead')
    else:
        sock.close()

def finish(result, pid):
    print 'in finish: %s' %(str(result.value))
    try:
        sendMail(email_address, 'huahai', 'SERVER DEAD!!!', '服务器没有回应心跳包')
        os.kill(int(pid), signal.SIGKILL)
    except Exception as e:
        print e
        reactor.stop()


if __name__ == '__main__':
    pid = os.popen('ps aux | grep \[b]abysiter.py').readline().split()[1]
    d = LoopingCall(testTcp).start(60)
    d.addErrback(finish, pid)
    reactor.run()

