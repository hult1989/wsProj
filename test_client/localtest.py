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

tcplocation = '3,1,190930141223,0000.00001W,0000.000001N,2623,0e92'
tcpaddsos = '2,98789,add42332112345'
tcpdelsos = '2,98789,del12332112345'
tcpimsi = '4,2,123150930141223'
tcpbind = '1,1028,bon1234567890,15882205392'
tcpdelete = '6,1023,ok'
tcpsync = '5,98789,3,7,12332112345,92332112345,1234321'




gpsrequest = dumps({'imei': '1024', 'timestamp': '1400030032000'})
bindrequest = dumps({'username': 'zod', 'simnum': '1234567890', 'name': '拐杖'})
imeirequest = dumps({'username': 'zod', 'simnum': '1234567890'})
setsosrequest = dumps({'imei': '98789', 'adminpwd': '123456', 'contactentry': {'sosnumber': '42332112345', 'contact':'蝙蝠侠'}})
delsosrequest = dumps({'imei': '98789', 'adminpwd': '123456', 'contactentry': {'sosnumber': '12332112345', 'contact':'蝙蝠侠'}})
varifyadd = dumps({'imei': '98789', 'sosnumber': '12332112345'})
varifydel = dumps({'imei': '98789', 'sosnumber': '12332112345'})
getsos = dumps({'imei': '98789'})
updatepwd = dumps({'imei': '2048', 'adminpwd': '123456', 'newadminpwd': '223456'})
register = dumps({'username': 'zod', 'password':'f'})
login = dumps({'username': 'zod', 'password':'f'})
upwd = dumps({'username': 'wonderwoman', 'password':'f', 'newpassword': 'g'})
newname = dumps({'username': 'zod', 'imei': '1024', 'name': '绿巨人'})
getstick = dumps({'username': 'zod'})
current = dumps({'username': 'zod', 'imei': '1024'})
upload = dumps({'username': 'zod', 'sticks': [{'name': 'hull', 'imei': '9981'}, {'name': 'del', 'imei': '1028'}] })
#rurequest = dumps({'username': 'zox', 'password': 'f', 'sticks': [{'name': 'hull', 'imei': '1024'}, {'name': 'del', 'imei': '1023'}] })
rurequest = dumps({'username': 'zoo', 'password':'f'})
#upload = dumps({'username': 'zod', 'sticks': [] })
getcoderequest = dumps({'username': 'alice', 'imei': '98789'})
unsubrequest = dumps({'username': 'zox', 'imei': '1024'})

host = 'http://localhost:8082/api'
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
unsubaddress = host + '/user?action=unsubscribe'
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



def testTcp(message):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8081)
    sock.connect(server_address)

    try:
        sock.sendall(message)
        data = sock.recv(96)
        print >> sys.stdout, 'RECEIVED: %s' % data
    finally:
        print >> sys.stdout, 'CLOSING SOCKET'
        sock.close()

def multiTest():
    try:
        server_address = ('localhost', 8081)
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect(server_address)
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect(server_address)

        location1 = '3,1025,150930141223,23.12321,87.22234'
        location2 = '3,1024,150930141223,23.12321W,87.22234N'
        sock1.sendall(location1)
        sock2.sendall(location2)
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

if sys.argv[1] == 'unsub':
    makeTest(unsubrequest, unsubaddress)

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
if sys.argv[1] == 'tcpdelall':
    testTcp(tcpdelete)
if sys.argv[1] == 'tcpsync':
    testTcp(tcpsync)
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

