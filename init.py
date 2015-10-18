from twisted.application import internet, service
from wsServer import WsServerFactory
from sqlPool import dbpool


application = service.Application('WalkingStickServer')
tcpService = internet.TCPServer(8081, WsServerFactory(dbpool))
tcpService.setServiceParent(application)
