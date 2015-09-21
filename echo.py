# -*- coding:utf-8 -*-
from twisted.python import log
from twisted.internet import protocol, reactor, defer, threads
from twisted.protocols import basic
from processData import processData
import time

class Echo(protocol.Protocol):
    #can add a log entry inside connectionMade
    def dataReceived(self, rawData):
        #it seems that some time-comsuming and cpu blocking operation can be warpped in Deferred funtion
        log.msg(rawData)
        d = threads.deferToThread(processRawData, rawData, self) 
        '''
        d.addCallback(getMsg)
        #the return value of getMsg will be passed to the next callback, aka sqlOperation in this case
        d.addErrback(onGetMsgError)
        d.addCallback(sqlOperation)
        d.addErrback(onSqlOperationError)

        '''
        d.addErrback(onError)
        #need parse and operate db here

class EchoFactory(protocol.Factory):
    protocol = Echo

def processRawData(data, echo):
    #processData requires many steps like get phone number, get message, database operation...each step require a callbacks and errbacks
    e = echo
    log.msg(data)
    processData(data)
    echo.transport.write('got your location')

    
    #data will be processed here, parse and put into database

def onError(failure):
    print failure


from sys import stdout
log.startLogging(stdout)
reactor.listenTCP(8081, EchoFactory())
reactor.run()
