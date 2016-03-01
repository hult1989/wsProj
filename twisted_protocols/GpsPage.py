# -*- coding:utf-8 -*-
from json import dumps

from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
from twisted.python import log, failure
from twisted.internet import defer, reactor

from appServerCommon import resultValue, onError, onSuccess
import appException
from sqlhelper import selectLocationSql
from sqlPool import wsdbpool
from OnlineStatusHelper import onlineStatusHelper


class GpsPage(Resource):
    isLeaf = True

    def getLegalPayload(self, request):
        payload = eval(request.content.read())
        imei = payload['imei']
        if not 'username' in payload:
            payload['username'] = 'anonym'
        lastsync = payload['timestamp']
        if len(imei) > 15 or len(imei) == 0 or len(lastsync) > 13 or len(lastsync) == 0 or lastsync.isdigit() == False:
            raise Exception('illegal input')
        return payload
        

    def render_POST(self, request):
        if request.args['action'] == ['getuserlocation']:
            try:
                payload = self.getLegalPayload(request)
                #log.msg(str(payload))
            except Exception, e:
                log.msg(e)
                return resultValue(300)

            d = selectLocationSql(wsdbpool, payload['imei'], payload['username'], payload['timestamp'], payload)
            d.addCallback(self.OnGpsResult, request, payload)
            d.addErrback(onError, request)
            if payload['imei'] in onlineStatusHelper.connectedSticks:
                onlineStatusHelper.connectedSticks[payload['imei']].updateAppRequestTime()
                log.msg(str(vars(onlineStatusHelper.connectedSticks[payload['imei']])))
            return NOT_DONE_YET
        elif request.args['action'] == ['switch']:
            payload = eval(request.content.read())
            if payload['oper'] == 'enable':
                if payload['imei'] not in onlineStatusHelper.connectedSticks:
                    return resultValue(509)
                status = onlineStatusHelper.connectedSticks[payload['imei']]
                status.transport.write('8,'+ payload['imei'] + ',1')
                d = status.switchGps(True).addCallbacks(onSuccess, onError, callbackArgs = (request,), errbackArgs=(request,))
                reactor.callLater(5, self.onSwitchOperTimeout, d)
                return NOT_DONE_YET


    def onSwitchOperTimeout(self, d):
        d.errback(failure.Failure(appException.StickOfflineException()))


    def OnGpsResult(self, result, request, payload):
        if len(result[0]) == 0:
            raise appException.NoMoreDataException
        else:
            locations = list()
            for r in result[0]:
                location = dict()
                location['longitude'] = str(r[1])
                location['latitude'] = str(r[2])
                location['timestamp'] = str(r[3]) + '000'
                location['type'] = str(r[4])
                location['imei'] = str(payload['imei'])
                if r[5]:
                    location['issleep'] = str(r[5])
                else:
                    location['issleep'] = '0'
                locations.append(location)
            request.write(dumps({'result': '1', 'imei': str(payload['imei']), 'locations': locations, 'opertime': str(result[1]) +  '000'}))
            request.finish()

gpsPage = GpsPage()
