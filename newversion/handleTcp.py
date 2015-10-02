# -*- coding:utf-8 -*-
from twisted.python import log
from twisted.internet import protocol, reactor, defer, threads
from twisted.protocols import basic
import time
import threading
from tcpPayloadOper import *

class Echo(protocol.Protocol):
    def dataReceived(self, message):
        if message[0] == '1':
            print message
            result = startBind(message)
        if message[0] == '2':
            result = insertSos(message)
        if message[0] == '3':
            result = insertLocation(message)
        if message[0] == '4':
            result = checkImsi(message)
        print result
        self.transport.write(result)


class EchoFactory(protocol.Factory):
    protocol = Echo

def onError(failure):
    print failure


from sys import stdout
log.startLogging(stdout)
log.startLogging(open('./echo.log', 'w'))
reactor.listenTCP(8081, EchoFactory())
reactor.run()
