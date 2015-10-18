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
            location['longitude'] = str(r[1])
            location['latitude'] = str(r[2])
            location['timestamp'] = str(r[3]) + '000'
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
    def onCurrentImei(self, result):
        if result == True:
            self.request.write(resultValue(1))
        else:
            self.request.write(resultValue(result))
        self.request.finish()

    def onGetCode(self, result):
        if result == 0:
            self.request.write(resultValue(403))
        else:
            self.request.write(dumps({'result': '1', 'code': str(result), 'imei': self.payload['imei']}))
        self.request.finish()

    def onGetImei(self, result):
        if result == 0:
            self.request.write(resultValue(601))
        else:
            self.request.write(dumps({'result': '1', 'imei': str(result)}))
        self.request.finish()

    def render_POST(self, request):
        self.request = request
        payload = eval(request.content.read())
        self.payload = payload
        log.msg(payload)
        if request.args['action'] == ['bind']:
            insertTempRelationSql(dbpool, simnum=payload['simnum'], username=payload['username']).addCallbacks(self.onBindResult, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['getimei']:
            selectRelationByUsernameSimnumSql(dbpool, payload['username'], payload['simnum']).addCallbacks(self.onImeiResult, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['setcurrentimei']:
            handleCurrentWsSql(dbpool, payload['username'], payload['imei']).addCallbacks(self.onCurrentImei, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['getverifycode']:
            createVefiryCodeSql(dbpool, payload['imei']).addCallbacks(self.onGetCode, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['getimeibycode']:
            getImeiByCodeSql(dbpool, payload['code']).addCallbacks(self.onGetImei, onError)
            return NOT_DONE_YET


class SosPage(Resource): 
    isLeaf = True
    def onSetResult(self, result):
        if result in ['402', '403', '505']:
            self.request.write(resultValue(result))
        else:
            self.request.write(resultValue(1))
        self.request.finish()

    def varifyPwd(self, result):
        log.msg('RESULT' + str(result))
        if len(result) == 0:
            d = defer.Deferred()
            d.callback('403')
            return d
        if result[0][2] == '0':
            d = defer.Deferred()
            d.callback('505')
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

    def varifyDel(self, result):
        if len(result) == 0:
            self.request.write(dumps({'result':'1', 'sosnumber':self.payload['sosnumber']}))
        self.request.finish()

    def onGetsos(self, result):
        if len(result) == 0:
            self.request.write(resultValue(503))
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
        if request.args['action'] == ['delnumber']:
            selectWsinfoSql(dbpool, payload['imei']).addCallback(self.varifyPwd).addCallbacks(self.onSetResult, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['varifyadd']:
            checkSosnumberSql(dbpool, payload['imei'], payload['sosnumber']).addCallbacks(self.varifySos, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['varifydel']:
            checkSosnumberSql(dbpool, payload['imei'], payload['sosnumber']).addCallbacks(self.varifyDel, onError)
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
            self.request.write(dumps({'result': '1', 'imei': result[0][1], 'name': result[0][2], 'simnum': result[0][3]}))
        elif type(result) == tuple and len(result) == 0:
            self.request.write(resultValue(404))
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
            return selectLoginInfoSql(dbpool, self.payload['username'])
        if self.request.args['action'] == ['updatepassword']:
            return UpdateUserPasswordSql(dbpool, username=self.payload['username'], newpassword=self.payload['newpassword'])
    
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
                stick['simnum'] = str(r[2])
                stick['name'] = str(r[1])
                stick['imei'] = str(r[0])
                sticks.append(stick)
            self.request.write(dumps({'result': '1', 'sticks': sticks}))
        self.request.finish()

    def onUpload(self, result):
        if result:
            self.request.write(resultValue(1))
        else:
            self.request.write(resultValue(403))
        self.request.finish()

    def render_POST(self, request):
        self.request = request
        payload = eval(request.content.read())
        self.payload = payload
        log.msg(payload)
        if request.args['action'] == ['register']:
            selectUserSql(dbpool, payload['username']).addCallback(self.checkUser).addCallbacks(self.onResult, onError)
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
        if request.args['action'] == ['uploadsticks']:
            handleUploadSql(dbpool, payload).addCallbacks(self.onUpload, onError)
            return NOT_DONE_YET


class LocationPage(Resource):
    isLeaf = True

    def render_GET(self, request):
        request.write("input imei")
        return """
        <html>
            <body>
                <form method="POST">
                    <input name="imei" type="text" />
                    <input type="submit" />
                </form>
            </body>
        </html>
        """

    def render_POST(self, request):
        self.request = request
        imei = str(cgi.escape(request.args["imei"][0]))
        dbpool.runQuery('select * from location where imei = %s', (imei,)).addCallbacks(self.onSuccess, self.onError)
        return NOT_DONE_YET
        
    def onSuccess(self, location):
        result = ''
        for i in location:
            result = result + str(i) + '</br>'

        self.request.write( """
        <html>
        <body>Location is: </br>%s</body>
        </html>
        """  % result)
        self.request.finish()

    
    def onError(self, error):
        log.msg(str(error))


class NumberPage(Resource):
    isLeaf = True

    def render_GET(self, request):
        request.write("input imei")
        return """
        <html>
            <body>
                <form method="POST">
                    <input name="imei" type="text" />
                    <input type="submit" />
                </form>
            </body>
        </html>
        """

    def render_POST(self, request):
        self.request = request
        imei = str(cgi.escape(request.args["imei"][0]))
        dbpool.runQuery('select * from sosnumber where imei = %s', (imei,)).addCallbacks(self.onSuccess, self.onError)
        return NOT_DONE_YET
        
    def onSuccess(self, numbers):
        result = ''
        for i in numbers:
            result = result + str(i) + '</br>'

        self.request.write( """
        <html>
        <body>numbers is: </br>%s</body>
        </html>
        """  % result)
        self.request.finish()

    
    def onError(self, error):
        log.msg(str(error))


class WsinfoPage(Resource):
    isLeaf = True

    def render_GET(self, request):
        request.write("input imei")
        return """
        <html>
            <body>
                <form method="POST">
                    <input name="imei" type="text" />
                    <input type="submit" />
                </form>
            </body>
        </html>
        """

    def render_POST(self, request):
        self.request = request
        imei = str(cgi.escape(request.args["imei"][0]))
        dbpool.runQuery('select * from wsinfo where imei = %s', (imei,)).addCallbacks(self.onSuccess, self.onError)
        return NOT_DONE_YET
        
    def onSuccess(self, numbers):
        result = ''
        for i in numbers:
            result = result + str(i) + '</br>'

        self.request.write( """
        <html>
        <body>wsinfo is: </br>%s</body>
        </html>
        """  % result)
        self.request.finish()

    
    def onError(self, error):
        log.msg(str(error))



if __name__ == '__main__':
    mainPage = Resource()
    apiPage = Resource()
    mainPage.putChild('api', apiPage)
    apiPage.putChild('gps', GpsPage())
    apiPage.putChild('stick', StickPage())
    apiPage.putChild('sos', SosPage())
    apiPage.putChild('user', UserPage())


    mainPage.putChild('location', LocationPage())
    mainPage.putChild('sos', NumberPage())
    mainPage.putChild('wsinfo', WsinfoPage())
    from sqlPool import dbpool
    #dbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456')
    #dbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456', unix_socket='/tmp/mysql.sock')

    #log.startLogging(open('app.log', 'w'))
    from sys import stdout
    log.startLogging(stdout)
    reactor.listenTCP(8082, Site(mainPage))
    reactor.run()
    
            



