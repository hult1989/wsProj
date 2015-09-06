from twisted.internet import protocol, reactor, defer
from twisted.protocols import basic
from processData import processData

class Echo(protocol.Protocol):
    def dataReceived(self, rawData):
        d = defer.Deferred()
        d.addCallback(processRawData)
        d.addErrback(onError)
        d.callback(rawData)
        #need parse and operate db here

class EchoFactory(protocol.Factory):
    protocol = Echo

def processRawData(data):
    processData(data)
    
    #data will be processed here, parse and put into database

def onError(failure):
    print failure


reactor.listenTCP(8081, EchoFactory())
reactor.run()
