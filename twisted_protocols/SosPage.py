# -*- coding:utf-8 -*-
from json import dumps, loads
from twisted.python import log
from twisted.internet import reactor, defer
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
import cgi

from SosModuleSql import *
from appServerCommon import onError, onSuccess, resultValue, appRequest
from sqlPool import wsdbpool


def nextMethod(result, method, *args):
    if method.func_name in ('checkImeiSimnumSql','selectSosNumberSql'):
        d = method(args[0], args[1])
    if method.func_name in ('deleteTempSosSql', 'checkAdminPwdSql', 'updateAdminPwdSql'):
        d = method(args[0], args[1], args[2])
    if method.func_name in ('insertTempSosSql', 'verifyOperSql', 'checkSosnumberSql'):
        d = method(args[0], args[1], args[2], args[3])
    return d


class SosPage(Resource): 
    isLeaf = True

    def onGetSos(self, result, request):
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
        log.msg(str(payload))
        apprequest = appRequest(payload)
        if apprequest.isValid == False:
            return resultValue(300)

        if request.args['action'] == ['addnumber']:
            d = checkAdminPwdSql(wsdbpool, payload['imei'], payload['adminpwd']).addCallback(nextMethod, checkImeiSimnumSql, wsdbpool, payload['imei']).addCallback(nextMethod, checkSosnumberSql, wsdbpool, payload['imei'], payload['contactentry']['sosnumber'], 'ADD').addCallback(nextMethod, insertTempSosSql, wsdbpool, payload['imei'], payload['contactentry']['sosnumber'], payload['contactentry']['contact'])
            d.addCallbacks(onSuccess, onError, callbackArgs=(request,), errbackArgs=(request,))
        
        elif request.args['action'] == ['delnumber']:
            d = checkAdminPwdSql(wsdbpool, payload['imei'], payload['adminpwd']).addCallback(nextMethod, checkImeiSimnumSql, wsdbpool, payload['imei']).addCallback(nextMethod, checkSosnumberSql, wsdbpool, payload['imei'],payload['contactentry']['sosnumber'], 'DEL').addCallback(nextMethod, insertTempSosSql, wsdbpool, payload['imei'], payload['contactentry']['sosnumber'], payload['contactentry']['contact'])
            d.addCallbacks(onSuccess, onError, callbackArgs=(request,), errbackArgs=(request,))

        elif request.args['action'] == ['varifyadd']:
            d = verifyOperSql(wsdbpool, payload['imei'], payload['sosnumber'], 'ADD')
            d.addCallbacks(onSuccess, onError, callbackArgs=(request,), errbackArgs=(request,))

        elif request.args['action'] == ['varifydel']:
            d = verifyOperSql(wsdbpool, payload['imei'], payload['sosnumber'], 'DEL')
            d.addCallbacks(onSuccess, onError, callbackArgs=(request,), errbackArgs=(request,))

        elif request.args['action'] == ['getnumber']:
            d = selectSosNumberSql(wsdbpool, payload['imei'])
            d.addCallbacks(self.onGetSos, onError, callbackArgs=(request,), errbackArgs=(request,))

        elif request.args['action'] == ['updatepassword']:
            d = checkAdminPwdSql(wsdbpool, payload['imei'], payload['adminpwd']).addCallback(nextMethod, updateAdminPwdSql, wsdbpool, payload['imei'], payload['newadminpwd'])
            d.addCallbacks(onSuccess, onError, callbackArgs=(request,), errbackArgs=(request,))

        return NOT_DONE_YET
           
sosPage = SosPage()
