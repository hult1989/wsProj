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
#tcplocation = '3,1024,160224015217,00000.00000,0000.00000,2540,7a8d,31,100,0,0,0,12'
msg = 'a,866523028123929,160101120000,00000.00000,0000.00000,050,1,1,0,0460,0000,0000,0007,27ba,0df5,0078,27ba,0f53,0068,27ba,0fbf,0082,27ba,0eda,0083,25f0,0e44,0086,27ba,0f1f,0087,27ba,0df4,0090,6'

#tcplocation = '3,867715029610974,160122075318,00000.000000,0000.000000,8008c,0065,13,098,0,0,0,31'
tcplocation = '3,1024,150930141223,0000.00000W,0000.000000N,2615,0e07,15,078,0,1\r\n'#3,1024,140930141223,0000.00000W,0000.000000N,2614,0e07,15,078,0\r\n3,1024,120930141223,0000.00000W,0000.000000N,2612,0e07,15,078,0\r\n3,1024,180930141223,0000.00000W,0000.000000N,2618,0e07,15,078,0\r\n3,1024,190930141223,0000.00000W,0000.000000N,2619,0e07,15,078,0\r\n3,1024,200930141223,0000.00000W,0000.000000N,2620,0e07,15,078,0\r\n3,1024,210930141223,0000.00000W,0000.000000N,2621,0e07,15,078,0\r\n3,1024,220930141223,0000.00000W,0000.000000N,2622,0e07,15,078,0\r\n3,1024,230930141223,0000.00000W,0000.000000N,2623,0e07,15,078,0\r\n3,1024,240930141223,0000.00000W,0000.000000N,2624,0e07,15,078,0\r\n3,1024,250930141223,0000.00000W,0000.000000N,2625,0e07,15,078,0\r\n3,1024,130930141223,0000.00000W,0000.000000N,2613,0e07,15,078,0\r\n3,1024,160930141223,0000.00000W,0000.000000N,2616,0e07,15,078,0\r\n3,1024,170930141223,0000.00000W,0000.000000N,2617,0e07,15,078,0\r\n'
#tcplocation = '3,867715029610974,130922141223,0000.00000W,0000.000000N,00a1,24b0,15\r\n3,867715029610974,140922141223,0000.00000W,0000.000000N,fffff,fffff,15\r\n3,867715029610974,150922141223,0000.00000W,0000.000000N,fffff,fffff,15\r\n3,867715029610974,160922141223,0000.00000W,0000.000000N,fffff,fffff,15\r\n3,867715029610974,170922141223,0000.00000W,0000.000000N,fffff,fffff,15\r\n'
tcpaddsos = '2,1027,add9989'
tcpdelsos = '2,8789,del12332112345'
tcpimsi = '4,98790,12332112345'
tcpbind = '1,98789,bon13836435683,15882205392'
tcpdelete = '6,1023,ok\r\n6,1023,ok'
tcpsync = '5,98789,3,7,12332112345,92332112345,22332112345'




gpsrequest = dumps({'imei': '1024', 'timestamp': '000',  'after': '1009226801000', 'before': '1959230401000', 'limit': '10' })
bindrequest = dumps({'username': 'zod', 'simnum': '0', 'name': '拐杖'})
imeirequest = dumps({'username': 'zod', 'simnum': '1234567890'})
setsosrequest = dumps({'imei': '1024', 'password': 'f', 'username': 'hulk', 'contactentry': {'sosnumber': '72332112345', 'contact':'蝙蝠侠'}})
delsosrequest = dumps({'imei': '1024', 'password': 'f', 'username': 'hulk', 'contactentry': {'sosnumber': '72332112345', 'contact':'蝙蝠侠'}})
varifyadd = dumps({'imei': '98789', 'sosnumber': '12332112345'})
varifydel = dumps({'imei': '98789', 'sosnumber': '12332112345'})
getsos = dumps({'imei': '862609000062401'})
updatepwd = dumps({'imei': '1024', 'adminpwd': '123456', 'newadminpwd': '223456'})
register = dumps({'username': 'zod', 'password':'f'})
login = dumps({'username': 'zod', 'password':'f'})
upwd = dumps({'username': 'wonderwoman', 'password':'f', 'newpassword': 'g'})
newname = dumps({'username': 'zod', 'imei': '1024', 'name': '绿巨人'})
getstick = dumps({'username': 'zod'})
current = dumps({'username': 'zod', 'imei': '1024'})
upload = dumps({'username': 'zod', 'sticks': [{'name': 'hull', 'imei': '9981'}, {'name': 'del', 'imei': '1028'}] })
review = dumps({'username': 'zod', 'review': '很好的app'})
#rurequest = dumps({'username': 'zox', 'password': 'f', 'sticks': [{'name': 'hull', 'imei': '1024'}, {'name': 'del', 'imei': '1023'}] })
rurequest = dumps({'username': 'zoo', 'password':'f'})
#upload = dumps({'username': 'zod', 'sticks': [] })
getcoderequest = dumps({'username': 'alice', 'imei': '98789'})
unsubrequest = dumps({'username': 'zox', 'imei': '1024'})
forgotpassword = dumps({'username': 'zoe'})
getemail = dumps({'username': 'lod'})
emailrequest = dumps({'username': '1025', 'email': 'kindth@qq.com'})
relatedusers = dumps({'imei': '19890924'})
deleteuser = dumps({'imei': '19890924', 'username': 'zod', 'deleteuser': 'alice'})
transferrequest = dumps({'imei': '1024', 'username': 'batman', 'newowner': 'hulk', 'password': 'b'})
setrelationship = dumps({'imei': '1029', 'username': 'bob', 'relationship': '我是你大爷'})
getrelationship = dumps({'imei': '1029', 'username': 'bob' })
switchrequest = dumps({'imei': '1024', 'oper': 'enable'})


host = 'http://localhost:8082/api'
gpsaddress = host + '/gps?action=getuserlocation'
switchaddress = host + '/gps?action=switch'
bindaddress = host + '/stick?action=bind'
imeiaddress = host + '/stick?action=getimei'
currentaddress = host + '/stick?action=setcurrentimei'
batteryaddress = host + '/stick?action=getbatterylevel'
transferaddress = host + '/stick?action=transferownership'
setrelationshipaddress = host + '/stick?action=setuserrelationship'
getrelationshipaddress = host + '/stick?action=getuserrelationship'
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
relatedaddress = host + '/stick?action=relatedusers'
deleteuseraddress = host + '/stick?action=deleteuser'
uploadaddress = host + '/user?action=uploadsticks'
unsubaddress = host + '/user?action=unsubscribe'
reviewaddress = host + '/user?action=review'
ruaddress = host + '/user?action=registerandupload'
updateaddress = host + '/user?action=updateapp'
checkaddress = host + '/user?action=checkemail'
emailaddress = host + '/user?action=fillinemail'
passwordaddress = host + '/user?action=forgotpassword'
getemailaddress = host + '/user?action=getemail'
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
    if sys.argv[1] == 'updateapp' or sys.argv[1] == 'checkemail':
        d = agent.request('GET', address, bodyProducer = StringProducer(request))
    else:
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
    message += '\r\n'

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

if sys.argv[1] == 'forgotpassword':
    makeTest(forgotpassword, passwordaddress)

if sys.argv[1] == 'unsub':
    makeTest(unsubrequest, unsubaddress)

if sys.argv[1] == 'users':
    makeTest(relatedusers, relatedaddress)

if sys.argv[1] == 'deleteuser':
    makeTest(deleteuser, deleteuseraddress)

if sys.argv[1] == 'updateapp':
    makeTest('asdfadsf', updateaddress)
if sys.argv[1] == 'checkemail':
    makeTest('asdfadsf', checkaddress)
if sys.argv[1] == 'review':
    makeTest(review, reviewaddress)
if sys.argv[1] == 'fillinemail':
    makeTest(emailrequest, emailaddress)

if sys.argv[1] == 'getemail':
    makeTest(getemail, getemailaddress)
if sys.argv[1] == 'gps':
    makeTest(gpsrequest, gpsaddress)
if sys.argv[1] == 'bind':
    makeTest(bindrequest, bindaddress)
if sys.argv[1] == 'tcpbind':
    testTcp(tcpbind)
if sys.argv[1] == 'tcplocation':
    testTcp(tcplocation)
if sys.argv[1] == 'newlocation':
    testTcp(msg)
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
if sys.argv[1] == 'getbattery':
    makeTest(getsos, batteryaddress)
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
if sys.argv[1] == 'transfer':
    makeTest(transferrequest, transferaddress)
if sys.argv[1] == 'setrelationship':
    makeTest(setrelationship, setrelationshipaddress)
if sys.argv[1] == 'getrelationship':
    makeTest(getrelationship, getrelationshipaddress)

if sys.argv[1] == 'switch':
    makeTest(switchrequest, switchaddress)

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

