# -*- coding:utf-8 -*-
from sqlhelper import *
from json import dumps, loads
from twisted.python import log
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
import cgi

def resultValue(n):
    return dumps({'result': str(n)})

def onError(failure):
    log.msg(failure)

class GpsPage(Resource):
    isLeaf = True

    def gpsResult(self, result):
        if len(result) == 0:
            self.request.write(resultValue(504))
            self.request.finish()
        
        locations = list()
        for r in result:
            location = dict()
            location['timestamp'] = r[0]
            location['longitude'] = r[1]
            location['latitude'] = r[2]
            locations.append(location)

        self.request.write(dumps({'result': '1', 'locations': locations}))
        self.request.finish()

            
    def render_POST(self, request):
        self.request = request
        payload = loads(request.content.read())
        selectLocationSql(dbpool, payload['imei'], payload['timestamp']).addCallbacks(self.gpsResult, onError)
        return NOT_DONE_YET


class StickPage(Resource):
    isLeaf = True
        
    def onBindResult(self, result):
        self.request.write(resultValue(1))
        self.request.finish()

    def onImeiResult(self, result):
        log.msg('RESULT' + str(result))
        if len(result) == 0:
            self.request.write(resultValue(501))
        else:
            self.request.write(dumps({'result':'1', 'imei': result[0][0]}))
        self.request.finish()

    def render_POST(self, request):
        self.request = request
        payload = eval(request.content.read())
        log.msg(payload)
        if request.args['action'] == ['bind']:
            insertTempRelationSql(dbpool, simnum=payload['simnum'], username=payload['username']).addCallbacks(self.onBindResult, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['getimei']:
            selectWsinfoBySimnum(dbpool, payload['simnum']).addCallbacks(self.onImeiResult, onError)
            return NOT_DONE_YET


class SosPage(Resource): 
    isLeaf = True
    def onSetResult(self, result):
        if result == '402' or result == '403':
            self.request.write(resultValue(result))
        else:
            self.request.write(resultValue(1))
        self.request.finish()

    def varifyPwd(self, result):
        if len(result) == 0:
            d = defer.Deferred()
            d.callback('403')
            return d
        if result[0][3] != self.payload['adminpwd']:
            d = defer.Deferred()
            d.callback('402')
            return d
        return insertTempSosSql(dbpool, imei=self.payload['imei'], sosnumber=self.payload['contactentry']['sosnumber'], contact=self.payload['contactentry']['contact'])
    
    def updatePwd(self, result):
        if len(result) == 0:
            d = defer.Deferred()
            d.callback('403')
            return d
        if result[0][3] != self.payload['adminpwd']:
            d = defer.Deferred()
            d.callback('402')
            return d
        return updateWsinfoPwdSql(dbpool, imei=self.payload['imei'], adminpwd=self.payload['newadminpwd'])
    
    def varifySos(self, result):
        if len(result) == 0:
            self.request.write(resultValue(501))
        else:
            self.request.write(dumps({'result':'1', 'sosnumber':result[0][1]}))
        self.request.finish()

    def onGetsos(self, result):
        if len(result) == 0:
            self.request.write(resultValue(403))
        else:
            contactentries = list()
            for r in result:
                contact = dict()
                contact['sosnumber'] = r[1]
                contact['contact'] = r[2]
                contactentries.append(contact)
            self.request.write(dumps({'result': '1', 'contactentries': contactentries}))
        self.request.finish()

            

    def render_POST(self, request):
        self.request = request
        payload = eval(request.content.read())
        self.payload = payload
        log.msg(payload)
        if request.args['action'] == ['addnumber']:
            selectWsinfoSql(dbpool, payload['imei']).addCallback(self.varifyPwd).addCallbacks(self.onSetResult, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['varifyadd']:
            checkSosnumberSql(dbpool, payload['imei'], payload['sosnumber']).addCallbacks(self.varifySos, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['getnumber']:
            selectSosnumberSql(dbpool, payload['imei']).addCallbacks(self.onGetsos, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['updatepassword']:
            selectWsinfoSql(dbpool, payload['imei']).addCallback(self.updatePwd).addCallbacks(self.onSetResult, onError)
            return NOT_DONE_YET

            

class UserPage(Resource):
    isLeaf = True

    def checkUser(self, result):
        if len(result) != 0:
            d = defer.Deferred()
            d.callback('400')
            return d
        else:
            return insertUserSql(dbpool, username=self.payload['username'], passwd=self.payload['password'])

    def onResult(self, result):
        if result in ['400', '401', '402', '403', '404']:
            self.request.write(resultValue(result))
        elif type(result) == tuple and len(result) != 0:
            self.request.write(dumps({'result': '1', 'imei': result[0][1], 'name': result[0][2]}))
        else:
            self.request.write(resultValue(1))
        self.request.finish()

    def onLogin(self, result):
        if len(result) == 0:
            d = defer.Deferred()
            d.callback('401')
            return d
        if self.payload['password'] != result[0][1]:
            d = defer.Deferred()
            d.callback('402')
            return d
        if self.request.args['action'] == ['login']:
            return selectDefaultRelationSql(dbpool, self.payload['username'])
        if self.request.args['action'] == ['updatepassword']:
            return UpdateUserPasswordSql(dbpool, username=self.payload['username'], newpassword=['newpassword'])
    
    def onChangeName(self, result):
        if len(result) == 0:
            return '403'
        else:
            return updateStickNameSql(dbpool, username=self.payload['username'], imei=self.payload['imei'], name=self.payload['name'])


    def onGetSticks(self, result):
        if len(result) == 0:
            self.request.write(resultValue(404))
        else:
            sticks = list()
            for r in result:
                stick = dict()
                stick['name'] = result[2]
                stick['imei'] = result[1]
                sticks.append(stick)
            self.request.write(dumps({'result': '1', 'sticks': sticks}))
        self.request.finish()

    def render_POST(self, request):
        self.request = request
        payload = eval(request.content.read())
        self.payload = payload
        log.msg(payload)
        if request.args['action'] == ['register']:
            d = selectUserSql(dbpool, payload['username']).addCallback(self.checkUser)
            d.addCallbacks(self.onResult, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['login']:
            selectUserSql(dbpool, payload['username']).addCallback(self.onLogin).addCallbacks(self.onResult, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['updatepassword']:
            selectUserSql(dbpool, payload['username']).addCallback(self.onLogin).addCallbacks(self.onResult, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['setstickname']:
            log.msg('GOINT TO CHANGE NAME')
            print ('GOINT TO CHANGE NAME')
            selectRelationByImeiSql(dbpool, payload['username'], payload['imei']).addCallback(self.onChangeName).addCallbacks(self.onResult, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['getsticks']:
            selectRelationSql(dbpool, payload['username']).addCallbacks(self.onGetSticks, onError)
            return NOT_DONE_YET






if __name__ == '__main__':
    mainPage = Resource()
    apiPage = Resource()
    mainPage.putChild('api', apiPage)
    apiPage.putChild('gps', GpsPage())
    apiPage.putChild('stick', StickPage())
    apiPage.putChild('sos', SosPage())
    apiPage.putChild('user', UserPage())

    dbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456')

    #log.startLogging(open('app.log', 'w'))
    from sys import stdout
    log.startLogging(stdout)
    reactor.listenTCP(8082, Site(mainPage))
    reactor.run()
    
            



