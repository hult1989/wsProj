from twisted.application import internet, service
from twisted.web import server
from echo import EchoFactory
from handlepost import FormPage

application = service.Application("ef", uid=1024, gid=1024)
serviceCollection = service.IServiceCollection(application)
internet.TCPServer(8081, EchoFactory()).setServiceParent(serviceCollection)
internet.TCPServer(8080, server.Site(FormPage())).setServiceParent(serviceCollection)
