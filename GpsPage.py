from twisted.web.resource import Resource
from appServerCommon import resultValue, onError
from sqlhelper import selectLocationSql
from sqlPool import dbpool
from twisted.web.server import Site, NOT_DONE_YET
from twisted.python import log
from json import dumps

class GpsPage(Resource):
    isLeaf = True

    def render_POST(self, request):
        payload = eval(request.content.read())
        d = selectLocationSql(dbpool, payload['imei'], payload['timestamp'])
        d.addCallback(self.OnGpsResult, request)
        d.addErrback(onError)
        return NOT_DONE_YET


    def OnGpsResult(self, result, request):
        if len(result) == 0:
            request.write(resultValue(504))
            request.finish()
        
        locations = list()
        for r in result:
            location = dict()
            location['longitude'] = str(r[1])
            location['latitude'] = str(r[2])
            location['timestamp'] = str(r[3]) + '000'
            locations.append(location)

        request.write(dumps({'result': '1', 'locations': locations}))
        request.finish()

            
gpsPage = GpsPage()
