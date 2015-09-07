from twisted.internet import protocol, reactor, defer
from twisted.protocols import basic
from processData import processData
from time import time
from noblocking import cc

class Echo(protocol.Protocol):
    def __init__(self):
        self.d = defer.Deferred()
    def dataReceived(self, rawData):
        print "receive data at:\t", time()
        #it seems that some time-comsuming and cpu blocking operation can be warpped in Deferred funtion
        self.d.addCallback(processRawData)
        '''
        d.addCallback(getMsg)
        #the return value of getMsg will be passed to the next callback, aka sqlOperation in this case
        d.addErrback(onGetMsgError)
        d.addCallback(sqlOperation)
        d.addErrback(onSqlOperationError)

        '''
        self.d.addErrback(onError)
        self.d.callback(rawData)
        print "goover callback at:\t", time()
        #need parse and operate db here

class EchoFactory(protocol.Factory):
    protocol = Echo

def processRawData(data):
    print "start process data at:\t", time()
    cc()
    #processData requires many steps like get phone number, get message, database operation...each step require a callbacks and errbacks
    processData(data)
    print "finish process data at:\t", time()
    
    #data will be processed here, parse and put into database

def onError(failure):
    print failure


reactor.listenTCP(8081, EchoFactory())
reactor.run()
