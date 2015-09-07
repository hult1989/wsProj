from twisted.internet import protocol, reactor, defer, threads
from twisted.protocols import basic
from processData import processData
import time

class Echo(protocol.Protocol):
    def dataReceived(self, rawData):
        print "response at:\t", time.time()
        #it seems that some time-comsuming and cpu blocking operation can be warpped in Deferred funtion
        d = threads.deferToThread(processRawData, rawData) 
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

def processRawData(data):
    time.sleep(5)
    #processData requires many steps like get phone number, get message, database operation...each step require a callbacks and errbacks
    processData(data)
    print "finish processing data at:\t", time.time()
    
    #data will be processed here, parse and put into database

def onError(failure):
    print failure


reactor.listenTCP(8081, EchoFactory())
reactor.run()
