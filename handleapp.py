# -*- coding:utf-8 -*-
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.python import log
from json import dumps, loads

from time import strftime
from chbasic import User
from sqlwriter import *
#from sqlwriter import createUser, authenticateUser, uploadSmokingData, getAllSmokingData, getSmokingDataByDate, updatePassword, rateApp, addFeedback
from openfireRest import createOpenfireUser

def register(request):
    payload = request.content.read()
    log.msg(payload)
    payload = loads(payload)
    username = payload['username']
    password = payload['password']
    gender = payload['gender']
    phone = payload['phone']
    email = payload['email']
    date = payload['date']
    user = User(username, password, gender, phone, email, date)
    createOpenfireUser(username, password)
    result, userid = createUser(user)
    jsonresult = dict()
    jsonresult['result'] = result
    d = dict()
    d['userid'] = userid
    jsonresult['detail'] = d
    return dumps(jsonresult) 


def login(request):
    payload = request.content.read()
    log.msg(payload)
    payload = loads(payload)
    username = payload['username']
    password = payload['password']
    result, detail = authenticateUser(username, password)
    jsonresult = dict()
    jsonresult['result'] = result
    if result == "1":
	    jsonresult['detail'] = loads(detail)
	    return dumps(jsonresult)
    elif result == "0":
            d = dict()
            d['reason'] = detail
            jsonresult['detail'] = d
            return dumps(jsonresult)

    
def updatePwd(request):
    payload = request.content.read()
    log.msg(payload)
    payload = loads(payload)
    username = payload['username']
    password = payload['password']
    newpwd = payload['newpassword']
    result, detail = updatePassword(username, password, newpwd)
    jsonresult = dict()
    jsonresult['result'] = result
    d = dict()
    d['reason'] = detail
    jsonresult['detail'] = d
    return dumps(jsonresult)


def giveFeedback(request):
    payload = request.content.read()
    payload = loads(payload)
    userid = payload['userid']
    feedback = payload['feedback']
    result = dict()
    detail = dict()
    result['result'], detail['resaon'] = addFeedback(userid, feedback)
    result['detail'] = detail
    return dumps(result)


def giveRate(request):
    payload = request.content.read()
    payload = loads(payload)
    userid = payload['userid']
    rating = int(payload['rating'])
    result = dict()
    detail = dict()
    result['result'], detail['resaon'] = rateApp(userid, rating)
    result['detail'] = detail
    return dumps(result)


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
        

class SmokingPage(Resource):
    isLeaf = True
    def render_POST(self, request):
        payload = request.content.read()
        log.msg(payload)
        payload = loads(payload)
        userid = payload['userid']
        date = payload['date']
        cigarnum = int(payload['cigarnum'])
        duration = int(payload['duration'])
        result, detail =  uploadSmokingData(userid, date, cigarnum, duration)
        d = dict()
        jsonresult = dict()
        jsonresult['result'] = result
        d['reason'] = detail
        jsonresult['detail'] = d
        return dumps(jsonresult)

class GetSmokingPage(Resource):
    isLeaf = True
    def render_POST(self, request):
        payload = request.content.read()
        log.msg(payload)
        payload = loads(payload)
        userid = payload['userid']
        date = payload['date']
        if len(date) == 0:
            result, cigarinfo =  getAllSmokingData(userid)
	    jsonresult = dict()
            if result == "0":
                jsonresult['result'] = result    
                reason = dict()
                reason['reason'] = cigarinfo
                jsonresult['detail'] = reason
                return dumps(jsonresult)
            jsonresult['result'] = result
            jsonresult['detail'] = cigarinfo
            return dumps(jsonresult)
        else:
            result, detail = getSmokingDataByDate(userid,  date)
	    jsonresult = dict()
            jsonresult['result'] = result
            cigarinfo = dict()
            if result == "0":
                cigarinfo['reason'] = detail    
                jsonresult['detail'] = cigarinfo 
                return dumps(jsonresult)
            cigarinfo['date'] = date
            cigarinfo['cigarnum'] = loads(detail)['cigarnum']
            cigarinfo['duration'] = loads(detail)['duration']
            jsonresult['detail'] = cigarinfo
            return dumps(jsonresult)

class UpdatePage(Resource):
    def render_GET(self, request):
	updateinfo = open('./updatefile/updateinfo.json', 'r')
        result = updateinfo.read()
        return result

class UploadPage(Resource):
    def render_POST(self, request):
        payload = loads(request.content.read())
        log.msg(payload)
        jsonresult = dict()
        detail = dict()

        try:
            log.msg('\ninsertEntry\n')
            insertEntry(payload['userid'], payload['date'], payload['cigartime'], payload['duration'])
            log.msg('\ngetUserTime\n')
            cigarnum, duration = getUserSmokingTime(payload['userid'], payload['date'])
            log.msg(cigarnum, duration)
            log.msg('\nupdateDatae\n')
            updateUserSmokingData(payload['userid'], payload['date'], cigarnum, duration)
            timestamp = strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            cigarinfo = dict()
            cigarinfo['date'] = payload['date']
            cigarinfo['duration'] = duration
            cigarinfo['cigarnum'] = cigarnum
            detail['cigarinfo'] = cigarinfo
            detail['timestamp'] = timestamp
            jsonresult['result'] = "1"
            jsonresult['detail'] = detail
            return dumps(jsonresult)
        except:
            detail['reason'] = "some error "
            jsonresult['result'] = "0"
            jsonresult['detail'] = detail
            return dumps(jsonresult)

class SyncPage(Resource):
    def render_POST(self, request):
        payload = loads(request.content.read())
        log.msg(payload)
        jsonresult = dict()
        detail = dict()

        try:
            values = getSync(str(payload['userid']), payload['timestamp'])
            log.msg(values)
            cigarinfo = dict()
            cigarinfolist = list()
            for i in values:
                item = dict()
                item['date'] = str(i[0])
                item['cigarnum'] = str(i[1])
                item['duration'] = str(i[2])
                cigarinfolist.append(item)
            detail['cigarinfo'] = cigarinfolist
            detail['timestamp'] = strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            jsonresult['result'] = '1'
            jsonresult['detail'] = detail
            return dumps(jsonresult)
        except:
            detail['reason'] = "some error "
            jsonresult['result'] = "0"
            jsonresult['detail'] = detail
            return dumps(jsonresult)



        


resource = Resource()
tempPage = Resource()
tempPage.putChild('api', resource)
resource.putChild('user', UserPage())
resource.putChild('getcigarinfo', GetSmokingPage())
resource.putChild('updatecigarinfo', SmokingPage())
resource.putChild('upload', UploadPage())
resource.putChild('sync', SyncPage())
resource.putChild('appupdate', UpdatePage())
from sys import stdout
#log.startLogging(open('server.log', 'w'))
log.startLogging(stdout)

factory = Site(tempPage)
reactor.listenTCP(8084, factory)
reactor.run()



