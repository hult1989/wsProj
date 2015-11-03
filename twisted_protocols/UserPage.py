from json import dumps, loads

from twisted.python import log
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET

import cgi

from appServerCommon import onError, resultValue
from sqlhelper import *
from sqlPool import wsdbpool


class UserPage(Resource):
    isLeaf = True

    def unSubSuccess(self, result, request, imei):
        request.write(dumps({'imei': imei, 'result': '1'}))
        request.finish()

    def unSubError(self, failure, request, imei):
        request.write(dumps({'imei': imei, 'result': str(failure.value.errCode)}))
        request.finish()



    def checkUser(self, result, payload):
        if len(result) != 0:
            d = defer.Deferred()
            d.callback('400')
            return d
        else:
            return insertUserSql(wsdbpool, username=payload['username'], passwd=payload['password'])

    def onResult(self, result, request):
        log.msg(str(result))
        if result in ['400', '401', '402', '403', '404']:
            request.write(resultValue(result))
        elif type(result) == tuple and len(result) != 0:
            request.write(dumps({'result': '1', 'imei': result[0][1], 'name': result[0][2], 'simnum': result[0][3]}))
        elif type(result) == tuple and len(result) == 0:
            request.write(resultValue(404))
        else:
            request.write(resultValue(1))
        request.finish()

    
    def onLogin(self, result, request, payload):
        if len(result) == 0:
            d = defer.Deferred()
            d.callback('401')
            return d
        if payload['password'] != result[0][1]:
            d = defer.Deferred()
            d.callback('402')
            return d
        if request.args['action'] == ['login']:
            return selectLoginInfoSql(wsdbpool, payload['username'])
        if request.args['action'] == ['updatepassword']:
            return UpdateUserPasswordSql(wsdbpool, username=payload['username'], newpassword=payload['newpassword'])

    def onRegister(self, result, request):
        if str(result) == '400':
            request.write(resultValue(result))
        else:
            request.write(resultValue('1'))

        request.finish()
        
    
    def onChangeName(self, result, payload):
        if len(result) == 0:
            return '403'
        else:
            return updateStickNameSql(wsdbpool, username=payload['username'], imei=payload['imei'], name=payload['name'])


    def onGetSticks(self, result, request):
        if len(result) == 0:
            request.write(resultValue(404))
        else:
            sticks = list()
            for r in result:
                stick = dict()
                stick['type'] = str(r[3])
                stick['simnum'] = str(r[2])
                stick['name'] = str(r[1])
                stick['imei'] = str(r[0])
                sticks.append(stick)
            request.write(dumps({'result': '1', 'sticks': sticks}))
        request.finish()

    def onUpload(self, result, request):
        if result:
            request.write(resultValue(1))
        else:
            request.write(resultValue(403))
        request.finish()

    def onRegisterUpload(self, result, request):
        if result == True:
            request.write(resultValue(1))
        elif result == 400:
            request.write(resultValue(400))
        request.finish()

    def render_POST(self, request):
        payload = eval(request.content.read())
        log.msg(str(payload))

        if request.args['action'] == ['register']:
            if 'username' not in payload or 'password' not in payload:
                return resultValue(300)
            if len(payload['username']) == 0 or len(payload['password']) == 0:
                return resultValue(300)
            d = selectUserSql(wsdbpool, payload['username']).addCallback(self.checkUser, payload)
            d.addCallback(self.onRegister, request)
            d.addErrback(onError)
            return NOT_DONE_YET
        if request.args['action'] == ['registerandupload']:
            if 'username' not in payload or 'password' not in payload:
                return resultValue(300)
            if 'sticks' in payload:
                for s in payload['sticks']:
                    if len(s['name']) == 0 or len(s['imei']) == 0:
                        return resultValue(300)
            handleRegisterandUploadSql(wsdbpool, payload).addCallbacks(self.onRegisterUpload, onError, callbackArgs=(request,))
            return NOT_DONE_YET
            


        if request.args['action'] == ['login']:
            if 'username' not in payload or 'password' not in payload:
                return resultValue(300)
            if len(payload['username']) == 0 or len(payload['password']) == 0:
                return resultValue(300)
            d = selectUserSql(wsdbpool, payload['username']).addCallback(self.onLogin, request, payload).addCallback(self.onResult, request)
            d.addErrback(onError)
            return NOT_DONE_YET
        if request.args['action'] == ['updatepassword']:
            if 'username' not in payload or 'password' not in payload or 'newpassword' not in payload:
                return resultValue(300)
            if len(payload['username']) == 0 or len(payload['newpassword']) == 0:
                return resultValue(300)
            d = selectUserSql(wsdbpool, payload['username']).addCallback(self.onLogin, request, payload).addCallback(self.onResult, request)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['setstickname']:
            if 'username' not in payload or 'imei' not in payload or 'name' not in payload:
                return resultValue(300)
            if len(payload['username']) == 0 or len(payload['name']) == 0 or len(payload['imei']) == 0:
                return resultValue(300)
            d = selectRelationByImeiSql(wsdbpool, payload['username'], payload['imei']).addCallback(self.onChangeName, payload)
            d.addCallback(self.onResult, request)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['getsticks']:
            if 'username' not in payload:
                return resultValue(300)
            d = selectRelationSql(wsdbpool, payload['username'])
            d.addCallback(self.onGetSticks, request)
            d.addErrback(onError)
            return NOT_DONE_YET

        if request.args['action'] == ['uploadsticks']:
            if 'username' not in payload or 'sticks' not in payload:
                return resultValue(300)
            if len(payload['username']) == 0 or len(payload['sticks']) == 0:
                return resultValue(300)
            for s in payload['sticks']:
                if len(s['name']) == 0 or len(s['imei']) == 0:
                    return resultValue(300)

            d = handleUploadSql(wsdbpool, payload)
            d.addCallback(self.onUpload, request)
            d.addErrback(onError)
            return NOT_DONE_YET
        
        if request.args['action'] == ['unsubscribe']:
            if 'username' not in payload or 'imei' not in payload:
                return resultValue(300)
            if len(payload['username']) == 0 or len(payload['imei']) == 0:
                return resultValue(300)
            d = handleUnsubscribeSql(wsdbpool, payload['username'], payload['imei']).addCallbacks(self.unSubSuccess, self.unSubError, callbackArgs=(request, payload['imei']), errbackArgs=(request, payload['imei']))
            d.addErrback(onError)
            return NOT_DONE_YET

userPage = UserPage()

