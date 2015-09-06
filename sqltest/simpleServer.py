from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
import json

class TestPage(Resource):
    isLeaf = True
    def render_POST(self, request):
        data =  json.loads(request.content.read())
        print data
        return data
        

resource = TestPage()
factory = Site(resource)
reactor.listenTCP(8080, factory)
reactor.run()
