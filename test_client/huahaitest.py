# -*- coding:utf-8 -*-
import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import Deferred, succeed, DeferredList
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.iweb import IBodyProducer
from zope.interface import implements
from json import dumps
import time


class StringProducer(object):
    implements(IBodyProducer)
    
    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass

class ResourcePrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished

    def dataReceived(self, data):
        #print time.time(), 'received data', data
        print data

    def connectionLost(self, reason):
        self.finished.callback(None)

def printResource(response):
    finished = Deferred()
    response.deliverBody(ResourcePrinter(finished))
    return finished


def stop(result):
    reactor.stop()

tcplocation = '3,1024,150930141223,0060.0000w,0006.0000s,2623,0e92'
tcpaddsos = '2,98789,add+12332112345'
tcpdelsos = '2,98789,del12332112345'
tcpimsi = '4,19890924,1401213873'
#tcpimsi = '4,867715029555583,46000260677419'
tcpbind = '1,19890924,15652963154,+8615885505392'



gpsrequest = dumps({'imei': '867715029635500', 'timestamp': '1400030032000'})
bindrequest = dumps({'username': '金刚狼', 'simnum': '15652963154', 'name': '爪子'})
imeirequest = dumps({'username': '金刚狼', 'simnum': '15652963154'})
setsosrequest = dumps({'imei': '98789', 'adminpwd': '123456', 'contactentry': {'sosnumber': '+12332112345', 'contact':'蝙蝠侠'}})
delsosrequest = dumps({'imei': '867715029551939', 'adminpwd': '123456', 'contactentry': {'sosnumber': '12332112345', 'contact':'蝙蝠侠'}})
varifyadd = dumps({'imei': '98789', 'sosnumber': '+12332112345'})
varifydel = dumps({'imei': '867715029551939', 'sosnumber': '13243725267'})
getsos = dumps({'imei': '1024'})
updatepwd = dumps({'imei': '2048', 'adminpwd': '123456', 'newadminpwd': '223456'})
register = dumps({'username': '金刚狼', 'password':'f'})
login = dumps({'username': '金刚狼', 'password':'f'})
upwd = dumps({'username': 'wonderwoman', 'password':'f', 'newpassword': 'g'})
newname = dumps({'username': 'zod', 'imei': '1024', 'name': '绿巨人'})
getstick = dumps({'username': 'zod'})
current = dumps({'username': 'zod', 'imei': '1024'})
upload = dumps({'username': 'zod', 'sticks': [{'name': 'hull', 'imei': '1024'}, {'name': 'del', 'imei': '1023'}] })
rurequest = dumps({'username': 'zox', 'password': 'f', 'sticks': [{'name': 'hull', 'imei': '1024'}, {'name': 'del', 'imei': '1023'}] })
#upload = dumps({'username': 'zod', 'sticks': [] })
getcoderequest = dumps({'username': 'alice', 'imei': '1024'})

host = 'http://huahai:8082/api'
gpsaddress = host + '/gps?action=getuserlocation'
bindaddress = host + '/stick?action=bind'
imeiaddress = host + '/stick?action=getimei'
currentaddress = host + '/stick?action=setcurrentimei'
setsosaddress = host + '/sos?action=addnumber'
delsosaddress = host + '/sos?action=delnumber'
varifyaddaddress = host + '/sos?action=varifyadd'
varifydeladdress = host + '/sos?action=varifydel'
getsosaddress = host + '/sos?action=getnumber'
updatepwdaddress = host + '/sos?action=updatepassword'
registeraddress = host + '/user?action=register'
loginaddress = host + '/user?action=login'
upwdaddress = host + '/user?action=updatepassword'
newnameaddress = host + '/user?action=setstickname'
getsticksaddress = host + '/user?action=getsticks'
getcodeaddress = host + '/stick?action=getverifycode'
getbycodeaddress = host + '/stick?action=getimeibycode'
uploadaddress = host + '/user?action=uploadsticks'
ruaddress = host + '/user?action=registerandupload'
subaddress = host + '/stick?action=subscribebycode'

agent = Agent(reactor)

def printResource(response):
    finished = Deferred()
    response.deliverBody(ResourcePrinter(finished))
    return finished

def printError(failure):
    import os
    print  failure
    #os.system('twistd -y init.py')
    print 'SERVE　RESTARTED'

def stop(result):
   # print time.time(), '\treactor stop'
    reactor.stop()

def makeTest(request, address):
    d = agent.request('POST', address, bodyProducer = StringProducer(request))
    d.addCallbacks(printResource, printError)
    d.addBoth(stop)
    reactor.run()
    

def asynchroTest(requests, addresses):
    dl = list()
    for z in zip(requests, addresses):
        d = agent.request('POST', z[1], bodyProducer=StringProducer(z[0]))
        d.addCallback(printResource)
        dl.append(d)
    deferList = DeferredList(dl, consumeErrors=True)
    deferList.addCallback(printResource)
    deferList.addBoth(stop)
    reactor.run()



import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('huahai', 8081)
sock.connect(server_address)

def testTcp(message):
    try:
        sock.sendall(message)
        data = sock.recv(96)
        print >> sys.stdout, 'RECEIVED: %s' % data
    finally:
        print >> sys.stdout, 'CLOSING SOCKET'
        sock.close()

def multiTest():
    try:
        server_address = ('huahai', 8081)
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect(server_address)
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect(server_address)

        location1 = '3,1024,150930141223,23.a12321,87.2b2234'
        location2 = '3,1024,150930141223,23.12321W,87.22234N'
        data1 = sock1.recv(96)
        data2 = sock1.recv(96)
        
        print >> sys.stdout, 'RECEIVED: %s' % data1
        print >> sys.stdout, 'RECEIVED: %s' % data2
    finally:
        print >> sys.stdout, 'CLOSING SOCKET'
        sock1.close()
        sock2.close()

if sys.argv[1] == 'multi':
    multiTest()

if sys.argv[1] == 'sub':
    code = sys.argv[2]
    subrequest = dumps({'username': 'hulk', 'name': 'needle', 'code': str(code)})
    makeTest(subrequest, subaddress)

if sys.argv[1] == 'ru':
    makeTest(rurequest, ruaddress)


if sys.argv[1] == 'gps':
    makeTest(gpsrequest, gpsaddress)
if sys.argv[1] == 'bind':
    makeTest(bindrequest, bindaddress)
if sys.argv[1] == 'tcpbind':
    testTcp(tcpbind)
if sys.argv[1] == 'tcplocation':
    testTcp(tcplocation)
if sys.argv[1] == 'getimei':
    makeTest(imeirequest, imeiaddress)
if sys.argv[1] == 'setsos':
    makeTest(setsosrequest, setsosaddress)
if sys.argv[1] == 'delsos':
    makeTest(delsosrequest, delsosaddress)
if sys.argv[1] == 'varifyadd':
    makeTest(varifyadd, varifyaddaddress)
if sys.argv[1] == 'varifydel':
    makeTest(varifydel, varifydeladdress)
if sys.argv[1] == 'getsos':
    makeTest(getsos, getsosaddress)
if sys.argv[1] == 'updatepwd':
    makeTest(updatepwd, updatepwdaddress)
if sys.argv[1] == 'register':
    makeTest(register, registeraddress)
if sys.argv[1] == 'current':
    makeTest(current, currentaddress)
if sys.argv[1] == 'login':
    try:
        makeTest(login, loginaddress)
    except Exception, e:
        print 'Server gone away, err msg: ', e
if sys.argv[1] == 'upwd':
    makeTest(upwd, upwdaddress)
if sys.argv[1] == 'newname':
    makeTest(newname, newnameaddress)
if sys.argv[1] == 'upload':
    makeTest(upload, uploadaddress)
if sys.argv[1] == 'getstick':
    makeTest(getstick, getsticksaddress)
if sys.argv[1] == 'tcpimsi':
    testTcp(tcpimsi)
if sys.argv[1] == 'tcpsetsos':
    testTcp(tcpaddsos)
if sys.argv[1] == 'tcpdelsos':
    testTcp(tcpdelsos)
if sys.argv[1] == 'getcode':
    makeTest(getcoderequest, getcodeaddress)
if sys.argv[1] == 'getbycode':
    makeTest(dumps({'code': str(sys.argv[2])}), getbycodeaddress)

if sys.argv[1] == 'gpspage':
    requests = list()
    for i in xrange(300):
        requests.append(register)
        requests.append(gpsrequest)
        requests.append(current)
    '''
    requests.append(upload)
    requests.append(getstick)
    requests.append(login)
    requests.append(gpsrequest)
    requests.append(current)
    requests.append(getsos)
    '''
    addresses = list()
    for i in xrange(300):
        addresses.append(registeraddress)
        addresses.append(gpsaddress)
        addresses.append(currentaddress)
    '''
    addresses.append(gpsaddress)
    addresses.append(currentaddress)
    addresses.append(getsosaddress)
    addresses.append(loginaddress)
    '''
    asynchroTest(requests, addresses)

