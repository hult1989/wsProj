# -*- coding:utf-8 -*-
from twisted.python import log
from twisted.internet import protocol, reactor, defer, threads
from twisted.protocols import basic
import time
from twisted.enterprise import adbapi
from sqlhelper import handleSosSql, handleBindSql, insertLocationSql, handleImsiSql

SQLUSER = 'tanghao'
PASSWORD = '123456'


def insertLocation(wsdbpool, message):
    message = message.split(',')
    imei = str(message[1]).strip()
    timestamp = '20'+ message[2].strip()
    longitude = message[3][:-1].strip()
    latitude = message[4][:-1].strip()
    if (message[3][-1] == 'W') or (message[3][-1] == 'w'):
        longitude = '-' + longitude
    if (message[4][-1] == 's') or (message[4][-1] == 'S'):
        latitude = '-' + latitude
    return insertLocationSql(wsdbpool, imei, longitude, latitude,  timestamp)




class WsServer(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        #log.msg('in wsServer, wsdbpool id: ' + str(id(self.factory.wsdbpool)))
    
    def onError(self, failure, transport, message):
        log.msg(failure)
        transport.write(''.join(("Result:", message[0], ',0')))

    def onSuccess(self, result, transport, message):
        if result == True or result == None or type(result) == tuple:
            transport.write(''.join(("Result:", message[0], ',1')))
        elif result == False:
            transport.write(''.join(("Result:", message[0], ',0')))


    def dataReceived(self, message):
        log.msg(message)
        #this is ok becase protocol is instantiated for each connection, so it won't has confusion
        if message[0] == '1':
            handleBindSql(self.factory.wsdbpool, message).addCallbacks(self.onSuccess, self.onError, callbackArgs=(self.transport, message), errbackArgs=(self.transport, message))
        if message[0] == '2':
            handleSosSql(self.factory.wsdbpool, message).addCallbacks(self.onSuccess, self.onError, callbackArgs=(self.transport, message), errbackArgs=(self.transport, message))
        if message[0] == '3':
            insertLocation(self.factory.wsdbpool, message).addCallbacks(self.onSuccess, self.onError, callbackArgs=(self.transport, message), errbackArgs=(self.transport, message))
        if message[0] == '4':
            handleImsiSql(self.factory.wsdbpool, message).addCallbacks(self.onSuccess, self.onError, callbackArgs=(self.transport, message), errbackArgs=(self.transport, message))



class WsServerFactory(protocol.Factory):
    def __init__(self, wsdbpool):
        self.wsdbpool = wsdbpool

    def buildProtocol(self, addr):
        return WsServer(self)

if __name__ == '__main__':
    from sqlPool import wsdbpool
    from sys import stdout
    #wsdbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456')
    log.startLogging(stdout)
    reactor.listenTCP(8081, WsServerFactory(wsdbpool))
    reactor.run()
