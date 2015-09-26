# -*- coding:utf-8 -*-
from twisted.python import log
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
import cgi
from sqlwriter import *
from walkingstickbasic import User, UserLocation, SOSNumberList
from json import dumps



def register(request):
    username = str(cgi.escape(request.args["username"][0]))
    password = str(cgi.escape(request.args["password"][0]))
    phone = str(cgi.escape(request.args["phone"][0]))
    newUser = User(phone = phone, username = username, password = password)
    newuserid = insertUser(newUser)
    

















class UserPage(Resource):
    isLeaf =  True
    def render_POST(self, request):
        if request.args['action'] == ['register']:
            return register(request)
        elif request.args['action'] == ['login']:
            return login(request)
        elif request.args['action'] == ['updatepassword']:
            return updatePwd(request)
        elif request.args['action'] == ['feedback']:
            return giveFeedback(request)
        elif request.args['action'] == ['rate']:
            return giveRate(request)
        




class GetLocationPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        request.write("input phone number")
        return """
        <html>
            <body>
                <form method="POST">
                    <input name="userid" type="text" />
                    <input type="submit" />
                </form>
            </body>
        </html>
        """

    def render_POST(self, request):
        userid = str(cgi.escape(request.args["userid"][0]))
        location = getLocation(userid)
        result = ''
        for i in location:
            result = result + dumps(vars(i)) + '</br>'

        return """
        <html>
        <body>Location is: </br>%s</body>
        </html>
        """  % result

class GetUserPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        print request.args
        request.write("input username")
        return """
        <html>
            <body>
                <form method="POST">
                    <input name="username" type="text" />
                    <input type="submit" />
                </form>
            </body>
        </html>
        """

    def render_POST(self, request):
        username = str(cgi.escape(request.args["username"][0]))
        user = getUserByName(username)
        result =  dumps(vars(user)) 
        print "YOUR SESSION IS:\t", request.getSession().uid
        return """
        <html>
        <body>Userinfo is: </br>%s</body>
        </html>
        """  % result

class GetNumberPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        log.msg(request.getSession().uid)
        request.write("input phone number")
        return """
        <html>
            <body>
                <form method="POST">
                    <input name="phone" type="text" />
                    <input type="submit" />
                </form>
            </body>
        </html>
        """

    def render_POST(self, request):
        phone = str(cgi.escape(request.args["phone"][0]))
        numberlist = getSOSNumberByPhone(phone)
        result = dumps(vars(numberlist)) 
        return """
        <html>
        <body>numberlist is: </br>%s</body>
        </html>
        """  % result

class RegisterPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        request.write("input userinfo")
        return """
        <html>
            <body>
                <form method="POST">
                   <p>
                   username: <input name="username" type="text" />
                   </p>
                   <p>
                   password: <input name="password" type="text" />
                   </p>
                   <p>
                   phone: <input name="phone" type="text" />
                   </p>
                    <input type="submit" />
                </form>
            </body>
        </html>
        """

    def render_POST(self, request):
        print request.content.read()
        username = str(cgi.escape(request.args["username"][0]))
        password = str(cgi.escape(request.args["password"][0]))
        phone = str(cgi.escape(request.args["phone"][0]))
        newUser = User(phone = phone, username = username, password = password)
        newuserid = insertUser(newUser)
        return """
        <html>
            <body>new userid is: </br>%s</body>
        </html>
        """  % newuserid 

class EditNumberPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        request.write("input userid(phone number)")
        return """
        <html>
            <body>
                <form method="POST">
                   <p>
                   userid: <input name="userid" type="text" />
                   </p>
                   <p>
                   sosnumbers: <input name="numbers" type="text" />
                   </p>
                   <input type="submit" />
                </form>
            </body>
        </html>
        """

    def render_POST(self, request):
        userid = str(cgi.escape(request.args["userid"][0]))
        numberlist = SOSNumberList(userid, str(cgi.escape(request.args["numbers"][0])))
        result = insertSOSNumber(numberlist)
        return """
        <html>
        <body>numberlist is: </br>%s</body>
        </html>
        """  % str(result)

class UploadPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        request.write("upload a file")
        return """
        <html>
            <body>
                <form method="POST">
                    <input name="upload" type="file" />
                    <input type="submit" />
                </form>
            </body>
        </html>
        """

    def render_POST(self, request):
        form =  cgi.FieldStorage()
        f = form.fp
        print 'file is:',  f.read()

    

mainPage = Resource()
tempPage = Resource()
tempPage.putChild('api', mainPage)
mainPage.putChild("getsos", GetNumberPage())
mainPage.putChild("getlocation", GetLocationPage())
mainPage.putChild("getuserinfo", GetUserPage())
mainPage.putChild("register", RegisterPage())
mainPage.putChild("editsosnumber", EditNumberPage())
mainPage.putChild("upload", UploadPage())


factory = Site(tempPage)
from sys import stdout
log.startLogging(stdout)
log.startLogging(open('handleweb.log', 'w'))
reactor.listenTCP(8082, factory)
reactor.run()
