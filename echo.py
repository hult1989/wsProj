# -*- coding:utf-8 -*-
from twisted.python import log
from twisted.internet import protocol, reactor, defer, threads
from twisted.protocols import basic
from processData import processData
from decoding import *
import time
import threading

class Echo(protocol.Protocol):
    #can add a log entry inside connectionMade
    def dataReceived(self, rawData):
        #it seems that some time-comsuming and cpu blocking operation can be warpped in Deferred funtion
        #log.msg(rawData)
        d = threads.deferToThread(processRawData, rawData, self) 
        '''
        d.addCallback(getMsg)
        #the return value of getMsg will be passed to the next callback, aka sqlOperation in this case
        d.addErrback(onGetMsgError)
        d.addCallback(sqlOperation)
        d.addErrback(onSqlOperationError)

        '''
        d.addErrback(onError)
        print 'FINISH dataReceived at:\t', time.ctime()
        #need parse and operate db here

class EchoFactory(protocol.Factory):
    protocol = Echo

def processRawData(data, echo):
    time.sleep(5)
    #processData requires many steps like get phone number, get message, database operation...each step require a callbacks and errbacks
    e = echo
    #log.msg(data)
    result = processData(data)
    response = createReturnValue(data, result)
    #log.msg(response)
    echo.transport.write(response)

    
    #data will be processed here, parse and put into database

def onError(failure):
    print failure


from sys import stdout
log.startLogging(stdout)
log.startLogging(open('./echo.log', 'w'))
reactor.listenTCP(8081, EchoFactory())
reactor.run()
