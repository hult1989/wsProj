from twisted.internet import protocol, reactor, defer, threads
from twisted.internet.task import LoopingCall
from twisted.protocols import basic
from processData import processData
from time import time, sleep
from noblocking import cc
from threading import currentThread


class Echo(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def dataReceived(self, rawData):
        self.factory.count += 1
        print "receive\t%d\t data at:%f" % (self.factory.count,  time())
        #it seems that some time-comsuming and cpu blocking operation can be warpped in Deferred funtion
        d = threads.deferToThread(processRawData, rawData)
        '''
        d.addCallback(getMsg)
        #the return value of getMsg will be passed to the next callback, aka sqlOperation in this case
        d.addErrback(onGetMsgError)
        d.addCallback(sqlOperation)
        d.addErrback(onSqlOperationError)

        '''
        d.addCallback(anotherCallback)
        d.addErrback(onError)
        print "thread callback at:\t", time()
        #need parse and operate db here

class EchoFactory(protocol.Factory):
    def __init__(self):
        self.count = 0
        print "Current Thread", currentThread()

    def buildProtocol(self, addr):
        return Echo(self)

def anotherCallback(data):
    print "another call back at:\t", time()

def processRawData(data):
    print "Current Thread", currentThread()
    sleep(5)
    #processData requires many steps like get phone number, get message, database operation...each step require a callbacks and errbacks
    processData(data)
    print "finish process data at:\t", time()
    
    #data will be processed here, parse and put into database

def onError(failure):
    print failure


reactor.listenTCP(8081, EchoFactory())
reactor.run()
