from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log

import cgi

class StatusPage(Resource):
    def __init__(self, onlineHelper):
        #super(Resource, self).__init__()
        self.onlineHelper = onlineHelper

    def onSwitch(self, result, request):
        print 'into web side on switch method'
        request.write('<html><body>stick %s gps is disabled </body></html>' %(imei))
        request.finish()

    def render_GET(self, request):
        return self.onlineHelper.getStatusWebPage()

    def render_POST(self, request):
        log.msg(str(request.args))
        if 'button' in request.args:
            imei = cgi.escape(request.args['button'][0])
            removePorts = []
            for port, status in self.onlineHelper.connectedSticks.items():
                if status.imei == imei:
                    self.onlineHelper.removePort(port)
                    removePorts.append(port.client)
            return '<html><body>stick %s is forced offline, removed connections %s</body></html>' %(imei, str(removePorts))

        elif 'disgps' in request.args:
            imei = cgi.escape(request.args['disgps'][0])
            for port, status in self.onlineHelper.connectedSticks.items():
                if status.imei == imei:
                    d = status.switchGps(False)
                    return '<html><body>stick %s gps is disabled, backward and refresh </body></html>' %(imei)
            return '<html><body>stick %s is not online</body></html>' %(imei)

                    

