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

'''
location = '3,123456789abcedf0,150930141223,23.12321W,87.22234N'
addsos = '2,2046,+15882205392'
delsos = '2,2046,-15882205392'
imsi = '4,123456789abcedf0,123150930141223'
bind = '1,123456789abcedf0,123150930141223,15882205392'
'''



gpsrequest = dumps({'imei': '1024', 'timestamp': '1400030032000'})
bindrequest = dumps({'username': 'alice', 'simnum': '13836435683'})
imeirequest = dumps({'username': 'alice', 'simnum': '13836435683'})
setsosrequest = dumps({'imei': '1029', 'adminpwd': '123456', 'contactentry': {'sosnumber': '13456412345', 'contact':'超人'}})
varifyadd = dumps({'imei': '1029', 'sosnumber': '13836435683'})
varifydel = dumps({'imei': '1024', 'sosnumber': '13836435683'})
getsos = dumps({'imei': '1224'})
updatepwd = dumps({'imei': '1324', 'adminpwd': '654321', 'newadminpwd': '123456'})
register = dumps({'username': 'uperman', 'password':'nicai'})
login = dumps({'username': 'alice', 'password':'g'})
upwd = dumps({'username': 'adice', 'password':'f', 'newpassword': 'g'})
newname = dumps({'username': 'adice', 'imei': '3', 'name': 'hulk'})
getstick = dumps({'username': 'alice'})

host = 'http://localhost:8082/api'
gpsaddress = host + '/gps?action=getuserlocation'
bindaddress = host + '/stick?action=bind'
imeiaddress = host + '/stick?action=getimei'
setsosaddress = host + '/sos?action=addnumber'
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
'''
    
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8081)
sock.connect(server_address)
log.startLogging(sys.stdout)
def testTcp(message):
    try:
        sock.sendall(message)
        data = sock.recv(96)
        print >> sys.stdout, 'RECEIVED: %s' % data
    finally:
        print >> sys.stdout.stderr, 'CLOSING SOCKET'
        sock.close()
'''

if sys.argv[1] == 'gps':
    makeTest(gpsrequest, gpsaddress)
if sys.argv[1] == 'bind':
    makeTest(bindrequest, bindaddress)
    import socket
if sys.argv[1] == 'getimei':
    makeTest(imeirequest, imeiaddress)
if sys.argv[1] == 'setsos':
    makeTest(setsosrequest, setsosaddress)
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
if sys.argv[1] == 'login':
    makeTest(login, loginaddress)
if sys.argv[1] == 'upwd':
    makeTest(upwd, upwdaddress)
if sys.argv[1] == 'newname':
    makeTest(newname, newnameaddress)
if sys.argv[1] == 'getstick':
    makeTest(getstick, getsticksaddress)
