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

    def onRegister(self, result):
        if str(result) == '400':
            self.request.write(resultValue(result))
        else:
            self.request.write(resultValue('1'))

        self.request.finish()
        
    
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
            selectUserSql(dbpool, payload['username']).addCallback(self.checkUser).addCallbacks(self.onRegister, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['login']:
            selectUserSql(dbpool, payload['username']).addCallback(self.onLogin).addCallbacks(self.onResult, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['updatepassword']:
            selectUserSql(dbpool, payload['username']).addCallback(self.onLogin).addCallbacks(self.onResult, onError)
            return NOT_DONE_YET
        if request.args['action'] == ['setstickname']:
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



from sqlPool import dbpool
mainPage = Resource()
apiPage = Resource()
mainPage.putChild('api', apiPage)
from GpsPage import gpsPage
apiPage.putChild('gps', gpsPage)
from StickPage import stickPage
apiPage.putChild('stick', stickPage)
from SosPage import sosPage
apiPage.putChild('sos', sosPage)
apiPage.putChild('user', UserPage())


mainPage.putChild('location', LocationPage())
mainPage.putChild('sos', NumberPage())
mainPage.putChild('wsinfo', WsinfoPage())


if __name__ == '__main__':
    #dbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456')
    #dbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456', unix_socket='/tmp/mysql.sock')

    #log.startLogging(open('app.log', 'w'))
    from sys import stdout
    log.startLogging(stdout)
    reactor.listenTCP(8082, Site(mainPage))
    reactor.run()
   
