from twisted.web.server import Site
from twisted.python import log
from twisted.internet import reactor
from twisted.web.resource import Resource

import sys
sys.path.append('./common')

from twisted_protocols.wsServer import WsServerFactory
from twisted_protocols.OnlineStatusHelper import onlineStatusHelper
from appServer import mainPage
from sqlPool import wsdbpool
from online import StatusPage, M2MPage
from logging_proxy import LoggingProxyFactory


if __name__ == '__main__':
    wsServerFactory = WsServerFactory(wsdbpool)
    log.startLogging(open('./log_file/server.log', 'a'))
    reactor.listenTCP(8000, LoggingProxyFactory())
    reactor.listenTCP(8081, wsServerFactory)
    reactor.listenTCP(8082, Site(mainPage))
    statusResource = Resource()
    statusResource.putChild('status', StatusPage(onlineStatusHelper))
    statusResource.putChild('m2m', M2MPage())
    reactor.listenTCP(8084, Site(statusResource))
    reactor.run()
