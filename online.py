# -*- coding:utf-8 -*-
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log

import cgi

class StatusPage(Resource):
    def __init__(self, onlineHelper):
        #super(Resource, self).__init__()
        self.onlineHelper = onlineHelper

    def onSwitch(self, result, request, imei):
        request.write('<html><body>stick %s gps is enabled/disabled </body></html>' %(imei))
        request.finish()

    def render_GET(self, request):
        return self.onlineHelper.getStatusWebPage()

    def render_POST(self, request):

        if 'enablegps' in request.args:
            log.msg('enable gps request from web ')
            imei = cgi.escape(request.args['imei'][0])
            if imei not in self.onlineHelper.connectedSticks:
                return '<html><body>stick %s is not online</body></html>' %(imei)
            status = self.onlineHelper.connectedSticks[imei]
            d = status.switchGps(True).addCallback(self.onSwitch, request, imei)
            return NOT_DONE_YET

        elif 'disgps' in request.args:
            log.msg('disable gps request from web ')
            imei = cgi.escape(request.args['imei'][0])
            if imei not in self.onlineHelper.connectedSticks:
                return '<html><body>stick %s is not online</body></html>' %(imei)
            status = self.onlineHelper.connectedSticks[imei]
            d = status.switchGps(False).addCallback(self.onSwitch, request, imei)
            return NOT_DONE_YET

        elif 'offline' in request.args:
            log.msg('force offline request from web')
            imei = cgi.escape(request.args['imei'][0])
            if imei not in self.onlineHelper.connectedSticks:
                return '<html><body>stick %s is not online</body></html>' %(imei)
            socket = str(self.onlineHelper.connectedSticks[imei].transport.client)
            self.onlineHelper.removeImei(imei)
            return '<html><body>stick %s at %s is forced offline</body></html>' %(imei, socket)

        return '<html><body>no item selected</body></html>' 


                    

class M2MPage(Resource):

    def render_POST(self, request):
        log.msg(request.content.read())
        return 'OK'

    render_GET = render_POST
