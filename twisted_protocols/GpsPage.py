# -*- coding:utf-8 -*-
from json import dumps

from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
from twisted.python import log

from appServerCommon import resultValue, onError
from sqlhelper import selectLocationSql
from sqlPool import wsdbpool

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
        try:
            payload = self.getLegalPayload(request)
            #log.msg(str(payload))
        except Exception, e:
            log.msg(e)
            return resultValue(300)

        d = selectLocationSql(wsdbpool, payload['imei'], payload['username'], payload['timestamp'], payload)
        d.addCallback(self.OnGpsResult, request, payload)
        d.addErrback(onError, request)
        return NOT_DONE_YET


    def OnGpsResult(self, result, request, payload):
        if len(result[0]) == 0:
            request.write(resultValue(504))
            request.finish()
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
