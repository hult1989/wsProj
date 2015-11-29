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
from pprint import pprint


#domain = 'smartcane.huahailife.com'
domain = 'localhost'
host =  domain + ':8082/api'
def stickSend(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (domain, 8081)
    sock.connect(server_address)
    #print message
    try:
        sock.sendall(message)
        data = sock.recv(96)
    finally:
        sock.close()
    #print data
    return str(data)


def appRequest(requestBody, url, method='POST'):
    #print requestBody
    con = httplib.HTTPConnection(domain, 8082)
    con.request(method, url, requestBody)
    result = con.getresponse().read()
    con.close()
    try:
        return eval(result)
    except Exception as e:
        print e
        return result
    
def stickSendImsi(imei, imsi='some Imsi'):
    tcpimsi = ','.join(('4', str(imei), str(imsi)))
    return stickSend(tcpimsi)

def stickBindAck(imei, simnum, appnum='+8615652963154'):
    tcpbind = ','.join(('1', str(imei), 'bon'+simnum , appnum))
    return stickSend(tcpbind)

def appBindRequest(username, simnum, name):
    bindaddress = '/api/stick?action=bind'
    bindrequest = dumps({'username': str(username), 'simnum': str(simnum), 'name': str(name)})
    result = appRequest(bindrequest, bindaddress)
    return result

def appGetBindImei(username, simnum):
    imeiaddress = '/api/stick?action=getimei'
    imeirequest = dumps({'username': str(username), 'simnum': str(simnum)})
    result = appRequest(imeirequest, imeiaddress)
    return result

def appGetAuthCode(username, imei):
    getcodeaddress = '/api/stick?action=getverifycode'
    getcoderequest = dumps({'username': str(username), 'imei': str(imei)})
    result = appRequest(getcoderequest, getcodeaddress)
    return result


def appGetStickList(username):
    address = '/api/user?action=getsticks'
    request = dumps({ 'username': str(username)})
    result = appRequest(request, address)
    return result

def otherAppSubByAuthCode(username, name, code):
    address = '/api/stick?action=subscribebycode'
    request = dumps({'code': str(code), 'username': str(username), 'name': str(name)})
    result = appRequest(request, address)
    return result

def appUnbind(username, imei):
    address = '/api/user?action=unsubscribe'
    request = dumps({'imei': str(imei), 'username': str(username)})
    result = appRequest(request, address)
    return result

def bindtest(username, imei, simnum, name):
    print stickSendImsi, stickSendImsi(imei)
    print appBindRequest, appBindRequest(username, simnum, name)
    print  stickBindAck, stickBindAck(imei, simnum)
    print appGetBindImei, appGetBindImei(username, simnum)

def subtest(username, imei, otheruser, name):
    result = appGetAuthCode(username, imei)
    print appGetAuthCode, '\n', result
    print otherAppSubByAuthCode, '\n', otherAppSubByAuthCode(otheruser, name, result['code'])
    
    

    

if __name__ == '__main__':
    #print appUnbind('zad', '19890924') 
    #print appUnbind('zod', '19890929') 
    print bindtest('zod', '19890929', '13836435683', 'birthday')
    #print subtest('zod', '19890929', 'xxx', 'alicezod')
    print dumps(appGetStickList('zod'), indent=1)
    #print dumps(appGetStickList('superman'), indent=1)

