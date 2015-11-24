from twisted.web.server import Site
from twisted.python import log
from twisted.internet import reactor

import sys
sys.path.append('./common')

from twisted_protocols.wsServer import WsServerFactory
from appServer import mainPage
from sqlPool import wsdbpool

if __name__ == '__main__':
    log.startLogging(open('./log_file/server.log', 'a'))
    reactor.listenTCP(8081, WsServerFactory(wsdbpool))
    reactor.listenTCP(8082, Site(mainPage))
    reactor.run()
