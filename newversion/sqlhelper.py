# -*- coding:utf-8 -*-
import mysql.connector
from wsbasic import *
import time
from twisted.internet import reactor, defer
from twisted.enterprise import adbapi
from twisted.python import failure

SQLUSER = 'tanghao'
PASSWORD = '123456'


def insertUserSql(dbpool, username, passwd, phone=None, email=None):
    return dbpool.runOperation('replace into userinfo (username, password, phone, email, date) values (%s, %s, %s, %s, CURDATE())', (username, passwd, phone, email))

def selectUserSql(dbpool, username):
    return dbpool.runQuery('select * from userinfo where username = %s', (username,))

def UpdateUserPasswordSql(dbpool, username, newpassword):
    return dbpool.runOperation('update userinfo set password = %s where username = %s', (newpassword, username))



def handleBindSql(dbpool, message):
    return dbpool.runInteraction(_handleBind, message)

def _handleBind(txn, message):
    message = message.split(',')
    imei = message[1]
    simnum = message[3]
    txn.execute('select username from temp_user_ws where simnum = %s', (simnum,))
    result = txn.fetchall()
    if len(result) == 0:
        return False
    username = result[0][0]
    txn.execute('replace into user_ws (username, imei, isdefault) values (%s, %s, "1")', (username, imei))
    txn.execute('delete from temp_user_ws where simnum = %s', (simnum,))
    txn.execute('replace into wsinfo (imei, imsi, simnum, adminpwd) values (%s, "", %s, "123456")', (imei, simnum))
    return True 




def handleSosSql(dbpool, message):
    return dbpool.runInteraction(_handleSos, message)

def _handleSos(txn, message):

    message = message.split(',')
    imei = message[1]
    sosnumber = message[2][1:]
    txn.execute('select * from temp_sos where imei = %s and sosnumber = %s', (imei, sosnumber))
    contactentry = txn.fetchall()[0]
    # sosnumber from walkingstick and what from app don't match
    if len(contactentry) == 0:
        return False
    
    if message[2][0] == '-':
        txn.execute('delete from sosnumber where imei = %s', (imei,))
    if message[2][0] == '+':
        txn.execute('replace into sosnumber (imei, sosnumber, contact) values (%s, %s, %s)', (contactentry[0], contactentry[1], contactentry[2]))

    txn.execute('delete from temp_sos where imei = %s and sosnumber = %s', (imei, sosnumber))
    return True 


def handleImsiSql(dbpool, message):
    return dbpool.runInteraction(_handleImsi, message)

def _handleImsi(txn, message):
    message = message.split(',')
    imei = message[1]
    imsi = message[2]
    txn.execute('select * from wsinfo where imei = %s', (imei,))
    result = txn.fetchall()
    if len(result) == 0:
        txn.execute('insert into wsinfo (imei, imsi, adminpwd) values(%s, %s, "123456")', (imei, imsi))
    else:
        txn.execute('update wsinfo set imsi = %s where imei = %s', (imsi, imei))
    txn.execute('select * from wsinfo where imei = %s', (imei,))
    return txn.fetchall()


    


def transactionTest(dbpool, username, passwd, phone=None, email=None):
    return dbpool.runInteraction(_interactionTest, username, passwd, phone, email)

def _interactionTest(txn, username, passwd, phone, email):
    txn.execute('replace into userinfo (username, password, phone, email, date) values (%s, %s, %s, %s, CURDATE())', (username, passwd, phone, email))
    txn.execute('select * from userinfo where username = %s', (username,))
    result = txn.fetchall()
    return result

def errTest(num):
    d = defer.Deferred()
    if num == 'a':
        '''
        here explictly callback already fired reactor and reactor will stop, it willnot stop in addCallback method
        '''
        d.errback(failure.Failure(TypeError('just error')))
    else:
        d.callback('hi body~')
    return d



def insertRelationSql(dbpool, username, imei, name=None, isdefault='1'):
    return dbpool.runOperation('replace into user_ws (username, imei, name, isdefault) values(%s, %s, %s, %s)', (username, imei, name, isdefault))

def selectRelationSql(dbpool, username):
    return dbpool.runQuery('select * from user_ws where username = %s', (username,))

def selectRelationByImeiSql(dbpool, username, imei):
    return dbpool.runQuery('select * from user_ws where username = %s and imei =%s', (username, imei))

def deleteRelationSql(dbpool, username, imei):
    return dbpool.runOperation('delete from user_ws where username = %s and imei = %s', (username, imei))

def selectDefaultRelationSql(dbpool, username):
    return dbpool.runQuery('select * from user_ws where username = %s and isdefault = "1"', (username,))

def updateStickNameSql(dbpool, username, imei, name):
    dbpool.runOperation('update user_ws set name = %s where username = %s and imei = %s', (name, username, imei))




def insertSosnumberSql(dbpool, imei, sosnumber, contact):
    return dbpool.runOperation('replace into sosnumber (imei, sosnumber, contact) values(%s, %s, %s)', (imei, sosnumber, contact))

def selectSosnumberSql(dbpool, imei):
    return dbpool.runQuery('select * from sosnumber where imei = %s', (imei,))

def deleteSosnumberSql(dbpool, imei, sosnumber):
    return dbpool.runOperation('delete from sosnumber where imei = %s and sosnumber = %s', (imei, sosnumber))


def checkSosnumberSql(dbpool, imei, sosnumber):
    return dbpool.runQuery('select * from sosnumber where imei = %s and sosnumber = %s', (imei, sosnumber))



def insertLocationSql(dbpool, imei, longitude, latitude, timestamp):
    return dbpool.runOperation('replace into location (imei, longitude, latitude, timestamp) values (%s, %s, %s, %s)', (imei, float(longitude), float(latitude), timestamp))

def selectWsinfoSql(dbpool, imei):
    return dbpool.runQuery('select * from wsinfo where imei = %s', (imei,))

def updateWsinfoPwdSql(dbpool, imei, adminpwd):
    return dbpool.runOperation('update wsinfo set adminpwd = %s where imei = %s', (adminpwd, imei))

def selectWsinfoBySimnum(dbpool, simnum):
    return dbpool.runQuery('select * from wsinfo where simnum = %s', (simnum,))


def insertWsinfoSql(dbpool, imei, imsi = None, simnum = None, adminpwd='123456'):
    return dbpool.runOperation('replace into wsinfo (imei, imsi, simnum, adminpwd) values (%s, %s, %s, %s)', (imei, imsi, simnum, adminpwd))

def selectLocationSql(dbpool, imei, timestamp):
    return dbpool.runQuery('select imei, longitude, latitude, unix_timestamp(timestamp) from location where imei = %s and unix_timestamp(timestamp) > %s', (imei, timestamp[0:-3]))




def insertTempRelationSql(dbpool, simnum, username):
    return dbpool.runOperation('replace into temp_user_ws (simnum, username) values( %s, %s)', (simnum, username))

def deleteTempRelationSql(dbpool, simnum):
    return dbpool.runOperation('delete from temp_user_ws where simnum = %s', (simnum,))

def selectTempRelationSql(dbpool, simnum):
    return dbpool.runQuery('select * from temp_user_ws where simnum = %s', (simnum,))




def insertTempSosSql(dbpool, imei, sosnumber, contact):
    return dbpool.runOperation('replace into temp_sos (imei, sosnumber, contact) values(%s, %s, %s)', (imei, sosnumber, contact))

def selectTempSosSql(dbpool, imei, sosnumber):
    return dbpool.runQuery('select * from temp_sos where imei = %s and sosnumber = %s', (imei, sosnumber))

def deleteTempSosSql(dbpool, imei, sosnumber):
    return dbpool.runOperation('delete from temp_sos where imei = %s and sosnumber = %s', (imei, sosnumber))




    '''
    print type(values)
    locations = []
    for v in values:
        locations.append({'imei': str(v[0]), 'longitude': str(float(v[1])), 'latitude': str(float(v[2])), 'timestamp': str(v[3])+'000' })
    return locations
    '''
   
def testResult(result):
    if type(result) == tuple and len(result) == 0:
        print 'No result'
    print result
    reactor.stop()

def testUtf(result):
    for r in result:
        for i  in r:
            print i
    reactor.stop()

def onSuccess(success):
    print success
    reactor.stop()

def onError(failure):
    print failure
    reactor.stop()


if __name__ == '__main__':
    import sys
    #dbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456', unix_socket='/tmp/mariadb3306.sock')
    dbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456')

    insertLocationSql(dbpool, '4321', '23.1298733', '12.1198712', '20151010120012').addCallback(onSuccess).addErrback(onError)


    '''
    if sys.argv[1] == 'insert':
        insertTempSosSql(dbpool, '1024', '+8615652963154', '超人').addCallback(testResult).addErrback(testResult)
    elif sys.argv[1] == 'delete':
        deleteTempSosSql(dbpool, '1024', '+8615652963154').addCallback(testResult).addErrback(testResult)
    else:
        handleBindSql(dbpool, '1,2046,asdflkj,15652963154').addCallback(onSuccess).addErrback(onError)

    insertTempRelationSql(dbpool, '15652963154', 'alice').addCallback(testResult).addErrback(testResult)
    selectTempRelationSql(dbpool, '15652963154').addCallback(testResult).addErrback(testResult)
    deleteTempRelationSql(dbpool, '15652963154').addCallback(testResult).addErrback(testResult)
    selectUserSql(dbpool, 'batman').addCallback(testResult).addErrback(testResult)
    deleteSosnumberSql(dbpool, '1024', '+8615652963154', ).addCallback(testResult).addErrback(testResult)
    deleteRelationSql(dbpool, 'alice', '0').addCallback(testResult).addErrback(testResult)
    insertRelationSql(dbpool, 'alice', '3', 'batman').addCallback(testResult).addErrback(testResult)
    selectRelationSql(dbpool, 'alice').addCallback(testResult).addErrback(testResult)
    selectSosnumberSql(dbpool, '1024').addCallback(testUtf).addErrback(testResult)
    insertSosnumberSql(dbpool, '1024', '+8615652963154', '超人').addCallback(testResult).addErrback(testResult)
    getLocationSql(dbpool, '4321', '1400000000000').addCallback(testResult).addErrback(testResult)
    insertWsinfoSql(dbpool, '1984').addCallback(testResult).addErrback(testResult)
    selectWsinfoSql(dbpool, '1984').addCallback(testResult).addErrback(testResult)
    selectLocationSql(dbpool, '4321', '1400000000').addCallback(testResult).addErrback(testResult)
    '''
    reactor.run()
