from twisted.application import internet, service
from wsServer import WsServerFactory
from appServer import mainPage
from sqlPool import dbpool
from twisted.web.server import Site


application = service.Application('WalkingStickServer')
sc = service.IServiceCollection(application)
appService = internet.TCPServer(8082, Site(mainPage))
tcpService = internet.TCPServer(8081, WsServerFactory(dbpool))
appService.setServiceParent(sc)
tcpService.setServiceParent(sc)
