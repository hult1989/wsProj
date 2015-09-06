import mysql.connector
from walkingstickbasic import User, UserLocation
import time


def executeSQL(sqlStr):
    connector = mysql.connector.connect(user='wswriter', password='f', database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sqlStr)
    connector.commit()
    cur.close()

def insertLocation(userlocation):
    sql = 'insert into location (userid, longitude, latitude, timestamp) values ("%s", "%f", "%f", "%s" );' % (userlocation.userid, userlocation.longitude, userlocation.latitude, userlocation.time)
    try:
        executeSQL(sql)
        return 1
    except e:
        return 0
    



def insertUser(user):
    sqlStr = 'insert into userinfo (username, password, time) values ("%s", "%s", "%s");' % (user.username, user.password, user.time )
    executeSQL(sqlStr)

def delUser(username):
    sqlStr = 'delete from userinfo where username = "%s";' % username
    executeSQL(sqlStr)

def getUser(username):
    sqlStr = 'select * from userinfo where username = "%s"; ' % username
    connector = mysql.connector.connect(user='wswriter', password='f', database = 'walkingstickdb', use_unicode=True)
    cur = connector.cursor()
    cur.execute(sqlStr)
    values = cur.fetchall()
    print len(values)
    user = User(id = values[0][0], username = str(values[0][1]), password = str(values[0][2]),time =  str(values[0][3]))
    cur.close()
    return user 


