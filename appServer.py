# -*- coding:utf-8 -*-
from sqlhelper import *
from json import dumps, loads
from twisted.python import log
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
import cgi

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
        wsdbpool.runQuery('select * from location where imei = %s', (imei,)).addCallbacks(self.onSuccess, self.onError)
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
        wsdbpool.runQuery('select * from sosnumber where imei = %s', (imei,)).addCallbacks(self.onSuccess, self.onError)
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
        wsdbpool.runQuery('select * from wsinfo where imei = %s', (imei,)).addCallbacks(self.onSuccess, self.onError)
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

from sqlPool import wsdbpool
from twisted_protocols.GpsPage import gpsPage
from twisted_protocols.StickPage import stickPage
from twisted_protocols.SosPage import sosPage
from twisted_protocols.UserPage import userPage

mainPage = Resource()
apiPage = Resource()
mainPage.putChild('api', apiPage)
apiPage.putChild('gps', gpsPage)
apiPage.putChild('stick', stickPage)
apiPage.putChild('sos', sosPage)
apiPage.putChild('user', userPage)

mainPage.putChild('location', LocationPage())
mainPage.putChild('sos', NumberPage())
mainPage.putChild('wsinfo', WsinfoPage())


if __name__ == '__main__':
    #wsdbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456')
    #wsdbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456', unix_socket='/tmp/mysql.sock')

    #log.startLogging(open('app.log', 'w'))
    from sys import stdout
    log.startLogging(stdout)
    reactor.listenTCP(8082, Site(mainPage))
    reactor.run()
   
