from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

import cgi

class StatusPage(Resource):
    def __init__(self, onlineHelper):
        self.onlineHelper = onlineHelper

    def render_GET(self, request):
        return self.onlineHelper.getStatusWebPage()

    def render_POST(self, request):
        imei = cgi.escape(request.args['button'][0])
        removePorts = []
        for port, status in self.onlineHelper.connectedSticks.items():
            if status.imei == imei:
                self.onlineHelper.removePort(port)
                removePorts.append(port.client)
        return '<html><body>stick %s is forced offline, removed connections %s</body></html>' %(imei, str(removePorts))


