from json import dumps, loads
from twisted.python import log
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
import cgi
from appServerCommon import onError, resultValue
from sqlhelper import *
from sqlPool import dbpool



class StickPage(Resource):
    isLeaf = True
        
    def onBindResult(self, result, request):
        request.write(resultValue(1))
        request.finish()

    def onImeiResult(self, result, request):
        log.msg('RESULT' + str(result))
        if len(result) == 0:
            request.write(resultValue(501))
        else:
            request.write(dumps({'result':'1', 'imei': result[0][0]}))
        request.finish()

    def onCurrentImei(self, result, request):
        if result == True:
            request.write(resultValue(1))
        else:
            request.write(resultValue(result))
        request.finish()

    def onGetCode(self, result, request, payload):
        if result == 0:
            request.write(resultValue(403))
        else:
            request.write(dumps({'result': '1', 'code': str(result), 'imei': payload['imei']}))
        request.finish()

    def onGetImei(self, result, request):
        if result == 0:
            request.write(resultValue(601))
        else:
            request.write(dumps({'result': '1', 'imei': str(result)}))
        request.finish()

    def render_POST(self, request):

        payload = eval(request.content.read())

        if request.args['action'] == ['bind']:
            if len(payload['username'])==0 or len(payload['simnum'])==0 or len(payload['name'])==0:
                return resultValue(300)
            d = insertTempRelationSql(dbpool, simnum=payload['simnum'], username=payload['username'], name=payload['name'])
            d.addCallback(self.onBindResult, request)
            d.addErrback(onError)
            return NOT_DONE_YET
        if request.args['action'] == ['getimei']:
            if len(payload['username'])==0 or len(payload['simnum'])==0:
                return resultValue(300)
            d = selectRelationByUsernameSimnumSql(dbpool, payload['username'], payload['simnum'])
            d.addCallback(self.onImeiResult, request)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['setcurrentimei']:
            if len(payload['imei']) == 0 or len(payload['username']) == 0:
                return resultValue(300)
            d = handleCurrentWsSql(dbpool, payload['username'], payload['imei'])
            d.addCallback(self.onCurrentImei, request)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['getverifycode']:
            if len(payload['imei']) == 0 or len(payload['username']) == 0:
                return resultValue(300)
            d = createVefiryCodeSql(dbpool, payload['imei'])
            d.addCallback(self.onGetCode, request, payload)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['getimeibycode']:
            d = getImeiByCodeSql(dbpool, payload['code'])
            d.addCallback(self.onGetImei, request)
            d.addErrback(onError)
            return NOT_DONE_YET

stickPage = StickPage()
