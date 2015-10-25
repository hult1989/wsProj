from wsServer import WsServerFactory
from appServer import mainPage
from twisted.web.server import Site
from twisted.python import log
from twisted.internet import reactor
from sqlPool import wsdbpool

if __name__ == '__main__':
    log.startLogging(open('./server.log', 'w'))
    reactor.listenTCP(8081, WsServerFactory(wsdbpool))
    reactor.listenTCP(8082, Site(mainPage))
    reactor.run()
