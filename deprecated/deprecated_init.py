from twisted.application import internet, service
from wsServer import WsServerFactory
from appServer import mainPage
from sqlPool import dbpool
from twisted.web.server import Site
from twisted.python import log

application = service.Application('WalkingStickServer')
sc = service.IServiceCollection(application)
log.startLogging(open('./server.log', 'w'))
appService = internet.TCPServer(8082, Site(mainPage))
tcpService = internet.TCPServer(8081, WsServerFactory(dbpool))
appService.setServiceParent(sc)
tcpService.setServiceParent(sc)
