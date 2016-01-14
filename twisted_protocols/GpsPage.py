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
        timestamp = payload['timestamp']
        if len(imei) > 15 or len(imei) == 0 or len(timestamp) > 13 or len(timestamp) == 0 or timestamp.isdigit == False:
            raise Exception('illegal input')
        return payload
        

    def render_POST(self, request):
        try:
            payload = self.getLegalPayload(request)
            log.msg(str(payload))
        except Exception, e:
            log.msg(e)
            return resultValue(300)

        d = selectLocationSql(wsdbpool, payload['imei'], payload['username'], payload['timestamp'])
        d.addCallback(self.OnGpsResult, request)
        d.addErrback(onError, request)
        return NOT_DONE_YET


    def OnGpsResult(self, result, request):
        if len(result) == 0:
            request.write(resultValue(504))
            request.finish()
        else:
            locations = list()
            for r in result:
                location = dict()
                location['longitude'] = str(r[1])
                location['latitude'] = str(r[2])
                location['timestamp'] = str(r[3]) + '000'
                location['type'] = str(r[4])
                if r[5]:
                    location['issleep'] = str(r[5])
                else:
                    location['issleep'] = '0'
                locations.append(location)
            request.write(dumps({'result': '1', 'locations': locations}))
            request.finish()

gpsPage = GpsPage()
