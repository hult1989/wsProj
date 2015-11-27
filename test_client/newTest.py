# -*- coding:utf-8 -*-
import sys
import httplib, socket
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import Deferred, succeed, DeferredList
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.iweb import IBodyProducer
from zope.interface import implements
from json import dumps
import time


domain = 'smartcane.huahailife.com'
host =  domain + ':8082/api'
def testTcp(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('smartcane.huahailife.com', 8081)
    sock.connect(server_address)
    print message
    try:
        sock.sendall(message)
        data = sock.recv(96)
    finally:
        sock.close()
    print data
    return str(data[9])


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


def makeRequest(requestBody, url, method='POST'):
    print requestBody
    con = httplib.HTTPConnection(domain, 8082)
    con.request(method, url, requestBody)
    result = con.getresponse().read()
    con.close()
    print result
    return eval(result)
    

def bindtest(username, imei, simnum, name):
    username = str(username)
    imei = str(imei)
    simnum = str(simnum)
    name  = str(name)
    bindaddress = '/api/stick?action=bind'
    imeiaddress = '/api/stick?action=getimei'
    tcpbind = ','.join(('1', imei, 'bon'+simnum , '+8615652963154'))
    bindrequest = dumps({'username': username, 'simnum': simnum, 'name': name})
    imeirequest = dumps({'username': username, 'simnum': simnum})
    result = makeRequest(bindrequest, bindaddress)
    assert result['result'] == '1'
    result = testTcp(tcpbind)
    assert result == '1'
    result = makeRequest(imeirequest, imeiaddress)
    print result

    

if __name__ == '__main__':
    print bindtest('zod', '98789', '13836435683', 'bid')

