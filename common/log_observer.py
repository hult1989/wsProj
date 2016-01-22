# -*- coding:utf-8 -*-
import os
import psutil
import time
from sendMail import sendMail

pid = os.popen('ps aux | grep \[i]nit.py').readline().split()[1]
address = 'kindth@qq.com'

def getSockNum(pid):
    connections = psutil.net_connections()
    nstick = 0
    napp = 0
    for c in connections:
        if c.laddr[1] == 8082:
            napp += 1
        elif c.laddr[1] == 8081:
            nstick += 1
    return nstick, napp


def sendSockInfo():
    nstick, napp = getSockNum(pid)
    sendMail(address, 'huahai', '出现EMFILE错误', '出现EMFILE错误，重启前拐杖端口和app端口sockets总数分别为:  %d 和 %d' %(nstick, napp))


def isEMFILEFound():
    while True:
        loginfo = os.popen('tail ./log_file/server.log').read()
        if loginfo.find('EMFILE') >= 0:
            print 'EMFILE ERROR FOUND'
        else:
            print 'everything normal'
        time.sleep(1)
    
isEMFILEFound()
