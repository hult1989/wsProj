import mysql.connector
from walkingstickbasic import SOSNumberList
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
    sql = 'insert into location (userid, longitude, latitude, timestamp) values ("%s", %f, %f, "%s" );' % (userlocation.userid, float(userlocation.longitude), float(userlocation.latitude), userlocation.timestamp)
    print sql
    try:
        executeSQL(sql)
        return 1
    except:
        return 0
 
def getLocation(userid):
    sqlStr = 'select * from location where userid = "%s"; ' % userid
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sqlStr)
    values = cur.fetchall()
    locationList = []
    for v in values:
        locationList.append(UserLocation(v[0], float(v[1]), float(v[2]), timestamp=v[3]))
    cur.close()
    return locationList

location = UserLocation('1', '23.1122', '31.342', '20150902132323')
print insertLocation(location)
ll =  getLocation('1')
for l in ll:
    print vars(l)


   
def getSOSNumber(userid):
    sql = 'select sosnumber from userinfo where userid = "%s";' % userid
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sql)
    values = cur.fetchall()
    cur.close()
    s = SOSNumberList(userid, values[0][0])
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





def insertUser(user):
    sqlStr = 'insert into userinfo (username, password, phone, date) values ("%s", "%s", "%s", CURDATE());' % (user.username, user.password, user.phone)
    executeSQL(sqlStr)
    newuser = getUserByName(user.username)
    return newuser.userid



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

def authenticateUser(username, pwd):
    sql = 'select userid, password from userinfo where username = "%s";' % username
    connector = mysql.connector.connect(user=SQLUSER, password=PASSWORD, database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sql)
    values = cur.fetchall()
    cur.close()
    if len(values) == 0:
        return "0", "no such user"
    userid = values[0][0]
    password = values[0][1]
    if pwd == password:
        return "1", userid
    return "0", "password error"


def updatePassword(username, password, newpassword):
    isAuthenticated = authenticateUser(username, password)
    if isAuthenticated[0] == "0":
        return isAuthenticated
    sql = 'update userinfo set password = "%s" where username = "%s";' % (newpassword, username)
    executeSQL(sql)
    return "1", "success"


u = User('alice', 'f', '15882205392')



'''
from json import dumps
s = getUser('alice')
#print dumps(vars(s))
s = getSOSNumber('15652963154')
#print dumps(vars(s))
'''

