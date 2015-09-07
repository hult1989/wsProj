import mysql.connector
from walkingstickbasic import User, UserLocation
import time

SQLUSER = 'wswriter'
PASSWORD = 'f'

def executeSQL(sqlStr):
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sqlStr)
    connector.commit()
    cur.close()

def insertLocation(userlocation):
    sql = 'insert into location (userid, longitude, latitude, timestamp) values ("%s", %f, %f, "%s" );' % (userlocation.userid, userlocation.longitude, userlocation.latitude, userlocation.timestamp)
    #print sql
    try:
        executeSQL(sql)
        return 1
    except e:
        return 0
    
def getSOSNumber(phone):
    sql = 'select sosnumber, id from userinfo where phone = "%s";' % phone
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sql)
    values = cur.fetchall()
    cur.close()
    s = SOSNumberList(userid = phone, numbers = values[0][0], id = values[0][1])
    return s


def insertSOSNumber(SOSNumberList):
    sql = 'update userinfo set sosnumber = "%s" where phone = "%s";' % (SOSNumberList.numbers, SOSNumberList.userid)
    executeSQL(sql)

def getLocation(userid):
    sqlStr = 'select * from location where userid = "%s"; ' % userid
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sqlStr)
    values = cur.fetchall()
    locationList = []
    for v in values:
        locationList.append(UserLocation(id=v[0], userid=v[1], longitude=v[2], latitude=v[3], timestamp=v[4]))
    cur.close()
    return locationList




def insertUser(user):
    sqlStr = 'insert into userinfo (username, password, phone, timestamp) values ("%s", "%s", "%s", "%s");' % (user.username, user.password, user.phone, user.timestamp )
    executeSQL(sqlStr)

def delUser(username):
    sqlStr = 'delete from userinfo where username = "%s";' % username
    executeSQL(sqlStr)

def getUser(username):
    sqlStr = 'select * from userinfo where username = "%s"; ' % username
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sqlStr)
    values = cur.fetchall()
    print values
    user = User(id = values[0][0], username = values[0][1], password = values[0][2],phone = values[0][3], timestamp = values[0][4])
    cur.close()
    return user 

from walkingstickbasic import SOSNumberList
from json import dumps
s = getUser('alice')
print dumps(vars(s))
s = getSOSNumber('15652963154')
print dumps(vars(s))
