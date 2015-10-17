# -*- coding:utf-8 -*-
import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import Deferred, succeed
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.iweb import IBodyProducer
from zope.interface import implements
from json import dumps


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
        print data

    def connectionLost(self, reason):
        self.finished.callback(None)

def printResource(response):
    finished = Deferred()
    response.deliverBody(ResourcePrinter(finished))
    return finished

def printError(failure):
    print >> sys.stderr, failure

def stop(result):
    reactor.stop()

tcplocation = '3,123456789abcedf0,150930141223,23.12321W,87.22234N'
tcpaddsos = '2,1024,+13456412345'
tcpdelsos = '2,1024,-15652963154'
tcpimsi = '4,123456789abcedf0,123150930141223'
tcpbind = '1,7878,11111111111,15882205392'



gpsrequest = dumps({'imei': '1024', 'timestamp': '1400030032000'})
bindrequest = dumps({'username': 'zod', 'simnum': '11111111111'})
imeirequest = dumps({'username': 'zod', 'simnum': '11111111111'})
setsosrequest = dumps({'imei': '1024', 'adminpwd': '123456', 'contactentry': {'sosnumber': '13836435683', 'contact':'蝙蝠侠'}})
delsosrequest = dumps({'imei': '1024', 'adminpwd': '123456', 'contactentry': {'sosnumber': '15652963154', 'contact':'蝙蝠侠'}})
varifyadd = dumps({'imei': '1024', 'sosnumber': '13836435683'})
varifydel = dumps({'imei': '1024', 'sosnumber': '15652963154'})
getsos = dumps({'imei': '1024'})
updatepwd = dumps({'imei': '1324', 'adminpwd': '654321', 'newadminpwd': '123456'})
register = dumps({'username': 'wonderwoman', 'password':'f'})
login = dumps({'username': 'superman', 'password':'f'})
upwd = dumps({'username': 'adice', 'password':'f', 'newpassword': 'g'})
newname = dumps({'username': 'alice', 'imei': '1024', 'name': '绿巨人'})
getstick = dumps({'username': 'zod'})
current = dumps({'username': 'alice', 'imei': '2012'})

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

agent = Agent(reactor)

def printResource(response):
    finished = Deferred()
    response.deliverBody(ResourcePrinter(finished))
    return finished

def printError(failure):
    print >> sys.stderr, failure

def stop(result):
    reactor.stop()

def makeTest(request, address):
    d = agent.request('POST', address, bodyProducer = StringProducer(request))
    d.addCallbacks(printResource, printError)
    d.addBoth(stop)
    reactor.run()
    
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8081)
sock.connect(server_address)

def testTcp(message):
    try:
        sock.sendall(message)
        data = sock.recv(96)
        print >> sys.stdout, 'RECEIVED: %s' % data
    finally:
        print >> sys.stdout, 'CLOSING SOCKET'
        sock.close()

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
    makeTest(login, loginaddress)
if sys.argv[1] == 'upwd':
    makeTest(upwd, upwdaddress)
if sys.argv[1] == 'newname':
    makeTest(newname, newnameaddress)
if sys.argv[1] == 'getstick':
    makeTest(getstick, getsticksaddress)
if sys.argv[1] == 'tcpimsi':
    testTcp(tcpimsi)
if sys.argv[1] == 'tcpsetsos':
    testTcp(tcpaddsos)
if sys.argv[1] == 'tcpdelsos':
    testTcp(tcpdelsos)
