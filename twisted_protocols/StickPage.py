from json import dumps, loads

from twisted.python import log
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
import cgi

from appServerCommon import onError, resultValue
from sqlhelper import *
from sqlPool import wsdbpool



class StickPage(Resource):
    isLeaf = True
        
    def onBindResult(self, result, request):
        request.write(resultValue(1))
        request.finish()

    def onImeiResult(self, result, request):
        if len(result) == 0:
            request.write(resultValue(501))
        else:
            request.write(dumps({'result':'1', 'imei': result[0][0], 'type': result[0][1]}))
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

    def onSubscribe(self, result, request):
        log.msg(str(result) + str(request))
        if result == 0:
            request.write(resultValue(601))
        else:
            request.write(dumps({'result': '1', 'imei': result[0], 'simnum': result[1], 'type': 's'}))
        request.finish()


    def render_POST(self, request):

        payload = eval(request.content.read())

        if request.args['action'] == ['bind']:
            if 'username' not in payload or 'simnum' not in payload or 'name' not in payload:
                return resultValue(300)
            if len(payload['username'])==0 or len(payload['simnum'])==0 or len(payload['name'])==0:
                return resultValue(300)
            d = insertTempRelationSql(wsdbpool, simnum=payload['simnum'], username=payload['username'], name=payload['name'])
            d.addCallback(self.onBindResult, request)
            d.addErrback(onError)
            return NOT_DONE_YET
        if request.args['action'] == ['getimei']:
            if 'username' not in payload or 'simnum' not in payload:
                return resultValue(300)
            if len(payload['username'])==0 or len(payload['simnum'])==0:
                return resultValue(300)
            d = selectRelationByUsernameSimnumSql(wsdbpool, payload['username'], payload['simnum'])
            d.addCallback(self.onImeiResult, request)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['setcurrentimei']:
            if 'imei' not in payload or 'username' not in payload:
                return resultValue(300)
            if len(payload['imei']) == 0 or len(payload['username']) == 0:
                return resultValue(300)
            d = handleCurrentWsSql(wsdbpool, payload['username'], payload['imei'])
            d.addCallback(self.onCurrentImei, request)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['getverifycode']:
            if 'imei' not in payload or 'username' not in payload:
                return resultValue(300)
            if len(payload['imei']) == 0 or len(payload['username']) == 0:
                return resultValue(300)
            d = createVefiryCodeSql(wsdbpool, payload['imei'])
            d.addCallback(self.onGetCode, request, payload)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['getimeibycode']:
            if 'code' not in payload or len(payload['code']) == 0:
                return resultValue(300)
            d = getImeiByCodeSql(wsdbpool, payload['code'])
            d.addCallback(self.onGetImei, request)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['subscribebycode']:
            if 'code' not in payload or len(payload['code']) == 0:
                return resultValue(300)
            if len(payload['code']) == 0:
                return resultValue(300)
            handleSubscribeByCodeSql(wsdbpool, payload).addCallbacks(self.onSubscribe, onError, callbackArgs=(request,))
            return NOT_DONE_YET

            


stickPage = StickPage()
