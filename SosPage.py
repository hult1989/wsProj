from json import dumps, loads
from twisted.python import log
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
import cgi
from appServerCommon import onError, resultValue
from sqlhelper import *
from sqlPool import wsdbpool


class SosPage(Resource): 

    isLeaf = True

    def onSetResult(self, result, request):
        if result in ['402', '403', '505']:
            request.write(resultValue(result))
        else:
            request.write(resultValue(1))
        request.finish()

    def varifyPwd(self, result, payload):
        if len(result) == 0:
            d = defer.Deferred()
            d.callback('403')
            return d
        if result[0][2] == '0':
            d = defer.Deferred()
            d.callback('505')
            return d
        if result[0][3] != payload['adminpwd']:
            d = defer.Deferred()
            d.callback('402')
            return d
        return insertTempSosSql(wsdbpool, imei=payload['imei'], sosnumber=payload['contactentry']['sosnumber'], contact=payload['contactentry']['contact'])
    
    def updatePwd(self, result, payload):
        if len(result) == 0:
            d = defer.Deferred()
            d.callback('403')
            return d
        if result[0][3] != payload['adminpwd']:
            d = defer.Deferred()
            d.callback('402')
            return d
        return updateWsinfoPwdSql(wsdbpool, imei=payload['imei'], adminpwd=payload['newadminpwd'])
    
    def varifySos(self, result, request):
        if len(result) == 0:
            request.write(resultValue(501))
        else:
            request.write(dumps({'result':'1', 'sosnumber':result[0][1]}))
        request.finish()

    def varifyDel(self, result, request, payload):
        if len(result) == 0:
            request.write(dumps({'result':'1', 'sosnumber':payload['sosnumber']}))
        request.finish()

    def onGetsos(self, result, request):
        if len(result) == 0:
            request.write(resultValue(503))
        else:
            contactentries = list()
            for r in result:
                contact = dict()
                contact['sosnumber'] = r[1]
                contact['contact'] = r[2]
                contactentries.append(contact)
            request.write(dumps({'result': '1', 'contactentries': contactentries}))
        request.finish()

            

    def render_POST(self, request):

        payload = eval(request.content.read())

        if request.args['action'] == ['addnumber']:
            if payload['imei'] == '0' or len(payload['imei']) == '0' or len(payload['contactentry']['sosnumber']) == 0 or payload['contactentry']['sosnumber'] == '0':
                return resultValue(300)
            d = selectWsinfoSql(wsdbpool, payload['imei']).addCallback(self.varifyPwd, payload)
            d.addCallback(self.onSetResult, request)
            d.addErrback(onError)
            return NOT_DONE_YET
        
        if request.args['action'] == ['delnumber']:
            if payload['imei'] == '0' or len(payload['imei'])== '0' or len(payload['contactentry']['sosnumber']) == 0 or payload['contactentry']['sosnumber'] == '0':
                return resultValue(300)
            d = selectWsinfoSql(wsdbpool, payload['imei']).addCallback(self.varifyPwd, payload)
            d.addCallback(self.onSetResult, request)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['varifyadd']:
            if payload['imei'] == '0' or len(payload['imei']) == '0' or len(payload['sosnumber']) == 0 or payload['sosnumber'] == '0':
                return resultValue(300)
            d = checkSosnumberSql(wsdbpool, payload['imei'], payload['sosnumber'])
            d.addCallback(self.varifySos, request)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['varifydel']:
            if payload['imei'] == '0' or len(payload['imei'] )== '0' or len(payload['sosnumber']) == 0 or payload['sosnumber'] == '0':
                return resultValue(300)
            d = checkSosnumberSql(wsdbpool, payload['imei'], payload['sosnumber'])
            d.addCallback(self.varifyDel, request, payload)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['getnumber']:
            d = selectSosnumberSql(wsdbpool, payload['imei'])
            d.addCallback(self.onGetsos, request)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['updatepassword']:
            if payload['imei'] == '0' or len(payload['imei']) == '0' or len(payload['newadminpwd']) == 0:
                return resultValue(300)
            d = selectWsinfoSql(wsdbpool, payload['imei']).addCallback(self.updatePwd, payload)
            d.addCallback(self.onSetResult, request)
            d.addErrback(onError)
            return NOT_DONE_YET

            
sosPage = SosPage()
