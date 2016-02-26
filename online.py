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
        log.msg(str(request.__class__))
        log.msg(str(request.args))

        if 'enablegps' in request.args:
            log.msg('enable gps request from web ')
            imei = cgi.escape(request.args['imei'][0])
            for port, status in self.onlineHelper.connectedSticks.items():
                if status.imei == imei:
                    d = status.switchGps(True).addCallback(self.onSwitch, request, imei)
                    return NOT_DONE_YET
            return '<html><body>stick %s is not online</body></html>' %(imei)

        elif 'disgps' in request.args:
            log.msg('disable gps request from web ')
            imei = cgi.escape(request.args['imei'][0])
            for port, status in self.onlineHelper.connectedSticks.items():
                if status.imei == imei:
                    d = status.switchGps(False).addCallback(self.onSwitch, request, imei)
                    return NOT_DONE_YET
            return '<html><body>stick %s is not online</body></html>' %(imei)

        elif 'offline' in request.args:
            log.msg('force offline request from web')
            imei = cgi.escape(request.args['imei'][0])
            removePorts = []
            for port, status in self.onlineHelper.connectedSticks.items():
                if status.imei == imei:
                    self.onlineHelper.removePort(port)
                    removePorts.append(port.client)
            return '<html><body>stick %s is forced offline, removed connections %s</body></html>' %(imei, str(removePorts))
        return '<html><body>no item selected</body></html>' 


                    

