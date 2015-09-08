from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
import cgi
from sqlwriter import getLocation, getSOSNumber, getUser, insertUser
from walkingstickbasic import User, UserLocation, SOSNumberList
from json import dumps

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
        user = getUser(username)
        result =  dumps(vars(user)) 

        return """
        <html>
        <body>Userinfo is: </br>%s</body>
        </html>
        """  % result

class GetNumberPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        request.write("input userid(phone number)")
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
        numberlist = getSOSNumber(userid)
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
        username = str(cgi.escape(request.args["username"][0]))
        password = str(cgi.escape(request.args["password"][0]))
        phone = str(cgi.escape(request.args["phone"][0]))
        from time import time
        timestamp = str(int(time()))
        newUser = User(phone = phone, username = username, password = password, timestamp = timestamp)
        newuserid = insertUser(newUser)
        return """
        <html>
            <body>new userid is: </br>%d</body>
        </html>
        """  % newuserid 

    

mainPage = Resource()
mainPage.putChild("getsos", GetNumberPage())
mainPage.putChild("getlocation", GetLocationPage())
mainPage.putChild("getuserinfo", GetUserPage())
mainPage.putChild("register", RegisterPage())

factory = Site(mainPage)
reactor.listenTCP(8082, factory)
reactor.run()
