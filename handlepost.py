from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
import cgi
from sqlwriter import getLocation
from json import dumps

class FormPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        request.write("input phone number")
        return """
        <html>
            <body>
                <form method="POST">
                    <input name="form-field" type="text" />
                    <input type="submit" />
                </form>
            </body>
        </html>
        """

    def render_POST(self, request):
        userid = str(cgi.escape(request.args["form-field"][0]))
        location = getLocation(userid)
        result = ''
        for i in location:
            result = result + dumps(vars(i)) + '</br>'

        return """
        <html>
        <body>Location is: </br>%s</body>
        </html>
        """  % result

factory = Site(FormPage())
reactor.listenTCP(8080, factory)
reactor.run()
