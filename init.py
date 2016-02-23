from twisted.web.server import Site
from twisted.python import log
from twisted.internet import reactor
from twisted.web.resource import Resource

import sys
sys.path.append('./common')

from twisted_protocols.wsServer import WsServerFactory
from appServer import mainPage
from sqlPool import wsdbpool
from online import StatusPage

if __name__ == '__main__':
    wsServerFactory = WsServerFactory(wsdbpool)
    log.startLogging(open('./log_file/server.log', 'a'))
    reactor.listenTCP(8081, wsServerFactory)
    reactor.listenTCP(8082, Site(mainPage))
    statusResource = Resource()
    statusResource.putChild('status', StatusPage(wsServerFactory.onlineHelper))
    reactor.listenTCP(8084, Site(statusResource))
    reactor.run()
