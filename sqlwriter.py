import mysql.connector
from walkingstickbasic import SOSNumberList
from walkingstickbasic import User, UserLocation
import time

SQLUSER = 'tanghao'
PASSWORD = '123456'

def executeSQL(sqlStr):
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sqlStr)
    connector.commit()
    cur.close()

def selectSQL(sql):
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sql)
    values = cur.fetchall()
    cur.close()
    return values

def insertLocation(imei, longitude, latitude, timestamp):
    sql = 'insert into location (imei, longitude, latitude, timestamp) values ("%s", %.8f, %.8f, "%s" );' % (userlocation.userid, float(userlocation.longitude), float(userlocation.latitude), userlocation.timestamp)
    print sql
    try:
        executeSQL(sql)
        return 1
    except:
        return 0
 
def getLocation(userid):
    sqlStr = 'select * from location where imei = "%s"; ' % userid
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sqlStr)
    values = cur.fetchall()
    locationList = []
    for v in values:
        locationList.append(UserLocation(v[0], float(v[1]), float(v[2]), timestamp=str(v[3])))
    cur.close()
    return locationList
   
def getSOSNumberByPhone(phone):
    sql = 'select sosnumber from userinfo where phone = "%s";' % phone
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sql)
    values = cur.fetchall()
    cur.close()
    if len(values) == 0:
        return "0", "no sos number"
    s = SOSNumberList(phone, values[0][0])
    return s



def insertSOSNumber(SOSNumberList):
    sql = 'update userinfo set sosnumber = "%s" where userid = "%s";' % (SOSNumberList.numbers, SOSNumberList.userid)
    try:
        executeSQL(sql)
        return "1", "success"
    except:
        return "0", "error"


s = SOSNumberList('1', '15882205392, 15652963154')
#print insertSOSNumber(s)
#print vars(getSOSNumber('1'))


def authenticateUser(username, password):
    sql = 'select userid, password from userinfo where username = "%s";' %username
    values = selectSQL(sql)
    if len(values) == 0:
        return {"result":"0", "detail":"no such user"}
    realpassword = str(values[0][1])
    if realpassword == password:
        return {"result":"1", "detail":{"userid":str(values[0][0])}}
    return {"result": "0", "detail": "password error"}
    



def insertUser(user):
    sqlStr = 'insert into userinfo (username, password, phone, date) values ("%s", "%s", "%s", CURDATE());' % (user.username, user.password, user.phone)
    executeSQL(sqlStr)
    newuser = getUserByName(user.username)
    return str(newuser.userid)



def delUser(username):
    sqlStr = 'delete from userinfo where username = "%s";' % username
    executeSQL(sqlStr)

def getUserByName(username):
    sqlStr = 'select userid, username, password, phone, date from userinfo where username = "%s"; ' % username
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sqlStr)
    values = cur.fetchall()
    #print values
    user = User(userid = values[0][0], username = values[0][1], password = values[0][2],phone = values[0][3])
    cur.close()
    return user 

def getUserByUserid(userid):
    sqlStr = 'select userid, username, password, phone, date from userinfo where userid = "%s"; ' % userid
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sqlStr)
    values = cur.fetchall()
    #print values
    user = User(userid = values[0][0], username = values[0][1], password = values[0][2],phone = values[0][3])
    cur.close()
    return user 

def getUserByPhone(phone):
    sqlStr = 'select userid, username, password, phone, date from userinfo where phone = "%s"; ' % phone
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sqlStr)
    values = cur.fetchall()
    #print values
    user = User(userid = values[0][0], username = values[0][1], password = values[0][2],phone = values[0][3])
    cur.close()
    return user 


def updatePassword(username, password, newpassword):
    isAuthenticated = authenticateUser(username, password)
    if isAuthenticated[0] == "0":
        return isAuthenticated
    sql = 'update userinfo set password = "%s" where username = "%s";' % (newpassword, username)
    executeSQL(sql)
    return "1", "success"

if __name__ == '__main__':
    u = User('alice', 'f', '15882205392')
    l = UserLocation('15882205392', '11.1123234', '11.112', '20150920112222')
    print authenticateUser('alice', 'x')


'''
from json import dumps
s = getUser('alice')
#print dumps(vars(s))
s = getSOSNumber('15652963154')
#print dumps(vars(s))
'''

