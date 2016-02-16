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


domain = 'smartcane.huahailife.com'
#domain = 'localhost'
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
    print data
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

def appNumber(imei, adminpwd, number, contact, numberType, oper):
    sosnumberRequest = dumps({'imei': str(imei), 'adminpwd': str(adminpwd), 'contactentry': {'sosnumber': str(number), 'contact': str(contact)}})
    familynumberRequest = dumps({'imei': str(imei), 'adminpwd': str(adminpwd), 'contactentry': {'familynumber': str(number), 'contact': str(contact)}})
    sosaddaddress = '/api/sos?action=addnumber'
    sosdeladdress = '/api/sos?action=delnumber'
    familyaddaddress = '/api/sos?action=addfamilynumber'
    familydeladdress = '/api/sos?action=delfamilynumber'
    if numberType == 's':
        if oper == 'ADD':
            result = appRequest(sosnumberRequest, sosaddaddress)
        elif oper == 'DEL':
            result = appRequest(sosnumberRequest, sosdeladdress)
    elif numberType == 'f':
        if oper == 'ADD':
            result = appRequest(familynumberRequest, familyaddaddress)
        elif oper == 'DEL':
            result = appRequest(familynumberRequest, familydeladdress)
    return result

def appPollingNumberResult(imei, number, oper, numberType):
    sosvarify = dumps({'imei': str(imei), 'sosnumber': str(number)})
    familyvarify = dumps({'imei': str(imei), 'familynumber': str(number)})
    sosaddaddress = '/api/sos?action=varifyadd'
    sosdeladdress = '/api/sos?action=varifydel'
    familyaddaddress = '/api/sos?action=varifyaddfamilynumber'
    familydeladdress = '/api/sos?action=varifydelfamilynumber'
    if numberType == 's':
        if oper == 'ADD':
            result = appRequest(sosvarify, sosaddaddress)
        elif oper == 'DEL':
            result = appRequest(sosvarify, sosdeladdress)
    elif numberType == 'f':
        if oper == 'ADD':
            result = appRequest(familyvarify, familyaddaddress)
        elif oper == 'DEL':
            result = appRequest(familyvarify, familydeladdress)
    return result

def appGetNumber(imei, numberType):
    sosaddress = '/api/sos?action=getnumber';
    familyaddress = '/api/sos?action=getfamilynumber';
    request = dumps({'imei': str(imei)})
    if numberType == 'f':
        return appRequest(request, familyaddress)
    else:
        return appRequest(request, sosaddress)

def stickCheckNumber(imei, number, oper, numberType):
    if oper == 'ADD':
        if numberType == 's':
            message = ','.join(('2', str(imei), 'add'+str(number) ))
        elif numberType == 'f':
            message = ','.join(('2', str(imei), 'adf'+str(number) ))
    elif oper == 'DEL':
        if numberType == 's':
            message = ','.join(('2', str(imei), 'del'+str(number) ))
        elif numberType == 'f':
            message = ','.join(('2', str(imei), 'def'+str(number) ))
    return stickSend(message)

def stickAckNumber(imei, numbers, numberType):
    if numberType == 'f':
        sync = ','.join(('7', str(imei), '3', '7', str(numbers[0]), str(numbers[1]), str(numbers[2])))
    else:
        sync = ','.join(('5', str(imei), '3', '7', str(numbers[0]), str(numbers[1]), str(numbers[2])))
    return stickSend(sync)


def numberTest(numberType, username, imei, number, contact, oper) :
    print appNumber(imei, '123456', number, contact, numberType, oper)
    print appPollingNumberResult(imei, number, oper, numberType)
    print stickCheckNumber(imei, number, oper, numberType)
    print stickAckNumber(imei, ('', '', '18688702834'), numberType)
    print appPollingNumberResult(imei, number, oper, numberType)
    print appGetNumber(imei, numberType)




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
    #print appNumber(862609000062401, 123456, 13609613781, 'bob', 'f', 'ADD')


    print appGetNumber(862609000062906, 's')
    print appGetNumber(862609000062906, 'f')
    #stickSend('3,868986022047287,000000000000,00000.00000E,0000.00000N,2495,1395,19,083,0')
    #print stickCheckNumber(98789, 9877912345, 'ADD', 's')
    #numberTest('s', 'zod', '1024', '18688702834', 'dan', 'ADD')
    #print stickAckNumber(98789, ('9877912345', '', ''), 's')
    #print appPollingNumberResult(98789, 9877912345, 'ADD', 's')
    #print appUnbind('zad', '19890924') 
    #print appUnbind('zod', '19890929') 
    #print bindtest('zod', '19890929', '13836435683', 'birthday')
    #print subtest('zod', '19890929', 'xxx', 'alicezod')
    #print dumps(appGetStickList('zod'), indent=1)
    #print dumps(appGetStickList('superman'), indent=1)

