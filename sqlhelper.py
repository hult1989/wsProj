# -*- coding:utf-8 -*-
import mysql.connector
import time
from twisted.internet import reactor, defer
from twisted.enterprise import adbapi
from twisted.python import failure
import random

SQLUSER = 'tanghao'
PASSWORD = '123456'

def createVefiryCodeSql(wsdbpool, imei):
    return wsdbpool.runInteraction(_createVerifyCode, imei)

def _createVerifyCode(txn, imei):
    txn.execute('select * from wsinfo where imei = %s', (imei,))
    if len(txn.fetchall()) == 0:
        return 0
    code = random.randint(100000, 999999)
    #delete timeout code
    txn.execute('delete from temp_code where unix_timestamp(timestamp) + 120 < unix_timestamp(now())', ())
    txn.execute('select * from temp_code where code = %s', (code,))
    result = txn.fetchall()
    while len(result) != 0:
        code = random.randint(100000, 999999)
        txn.execute('select * from temp_code where code = %s', (code,))
        result = txn.fetchall()
    txn.execute('insert into temp_code (code, imei) values(%s, %s)', (code, imei))
    return code


def getImeiByCodeSql(wsdbpool, code):
    return wsdbpool.runInteraction(_getImeiByCode, code)

def _getImeiByCode(txn, code):
    txn.execute('delete from temp_code where unix_timestamp(timestamp) + 120 < unix_timestamp(now())', ())
    txn.execute('select imei from temp_code where code = %s', (code,))
    result = txn.fetchall()
    if len(result) == 0:
        return 0
    return result[0][0]
    
def insertUserSql(wsdbpool, username, passwd, phone=None, email=None):
    return wsdbpool.runOperation('replace into userinfo (username, password, phone, email, date) values (%s, %s, %s, %s, CURDATE())', (username, passwd, phone, email))

def selectUserSql(wsdbpool, username):
    return wsdbpool.runQuery('select * from userinfo where username = %s', (username,))

def UpdateUserPasswordSql(wsdbpool, username, newpassword):
    return wsdbpool.runOperation('update userinfo set password = %s where username = %s', (newpassword, username))

def selectLoginInfoSql(wsdbpool, username):
    return wsdbpool.runQuery('select user_ws.username, user_ws.imei, user_ws.name, wsinfo.simnum from user_ws, wsinfo where user_ws.imei = wsinfo.imei and user_ws.username = %s and user_ws.isdefault = 1', (username,))


def handleBindSql(wsdbpool, message):
    return wsdbpool.runInteraction(_handleBind, message)

def _handleBind(txn, message):
    message = message.split(',')
    imei = message[1]
    simnum = message[2]
    userphone = message[3]
    txn.execute('select username, name from temp_user_ws where simnum = %s', (simnum,))
    result = txn.fetchall()
    if len(result) == 0:
        return False
    username = result[0][0]
    name = result[0][1]
    txn.execute('update userinfo set phone = %s where username = %s', (userphone, username))
    txn.execute('replace into user_ws (username, imei, name, isdefault) values (%s, %s, %s, "1")', (username, imei, name))
    txn.execute('delete from temp_user_ws where simnum = %s', (simnum,))
    txn.execute('replace into wsinfo (imei, imsi, simnum, adminpwd) values (%s, "", %s, "123456")', (imei, simnum))
    return True 




def handleSosSql(wsdbpool, message):
    return wsdbpool.runInteraction(_handleSos, message)

def _handleSos(txn, message):

    message = message.split(',')
    imei = message[1]
    sosnumber = message[2][1:]
    txn.execute('select * from temp_sos where imei = %s and sosnumber = %s', (imei, sosnumber))
    contactentry = txn.fetchall()
    # sosnumber from walkingstick and what from app don't match
    if len(contactentry) == 0:
        return False
    contactentry = contactentry[0]
    if message[2][0] == '-':
        txn.execute('delete from sosnumber where imei = %s and sosnumber = %s', (imei,sosnumber))
    if message[2][0] == '+':
        txn.execute('replace into sosnumber (imei, sosnumber, contact) values (%s, %s, %s)', (contactentry[0], contactentry[1], contactentry[2]))

    txn.execute('delete from temp_sos where imei = %s and sosnumber = %s', (imei, sosnumber))
    return True 


def handleImsiSql(wsdbpool, message):
    return wsdbpool.runInteraction(_handleImsi, message)

def _handleImsi(txn, message):
    message = message.split(',')
    imei = message[1]
    imsi = message[2]
    txn.execute('select * from wsinfo where imei = %s', (imei,))
    result = txn.fetchall()
    if len(result) == 0:
        txn.execute('insert into wsinfo (imei, imsi, adminpwd) values(%s, %s, "123456")', (imei, imsi))
    elif result[0][1] != imsi:
        txn.execute('update wsinfo set imsi = %s, simnum = 0 where imei = %s', (imsi, imei))
    txn.execute('select * from wsinfo where imei = %s', (imei,))
    return txn.fetchall()


    
def handleCurrentWsSql(wsdbpool, username, imei):
    return wsdbpool.runInteraction(_handleCurrentWs, username, imei)

def _handleCurrentWs(txn, username, imei):
    txn.execute('select imei from user_ws where isdefault = "1" and username = %s', (username,))
    result = txn.fetchall()
    if len(result) == 0:
        return 404
    for r in result:
        txn.execute('update user_ws set isdefault = "0" where username = %s and imei = %s', (username, r[0]))
    txn.execute('update user_ws set isdefault = "1" where username = %s and imei = %s', (username, imei))
    return True
    

def handleUploadSql(wsdbpool, payload):
    return wsdbpool.runInteraction(_handleUpload, payload)

def _handleUpload(txn, payload):
    for stick in payload['sticks']:
        txn.execute('replace into user_ws (username, imei, name, isdefault) values (%s, %s, %s, "0")', (payload['username'], stick['imei'], stick['name']))
    txn.execute('replace into user_ws (username, imei, name, isdefault) values (%s, %s, %s, "1")', (payload['username'], payload['sticks'][-1]['imei'], payload['sticks'][-1]['name']))
    return True



def insertRelationSql(wsdbpool, username, imei, name=None, isdefault='1'):
    return wsdbpool.runOperation('replace into user_ws (username, imei, name, isdefault) values(%s, %s, %s, %s)', (username, imei, name, isdefault))

def selectRelationSql(wsdbpool, username):
    return wsdbpool.runQuery('select  wsinfo.imei, user_ws.name, wsinfo.simnum from user_ws, wsinfo where user_ws.imei = wsinfo.imei and user_ws.username = %s', (username,))

def selectRelationByImeiSql(wsdbpool, username, imei):
    return wsdbpool.runQuery('select * from user_ws where username = %s and imei =%s', (username, imei))

def selectRelationByUsernameSimnumSql(wsdbpool, username, simnum):
    return wsdbpool.runQuery('select wsinfo.imei from user_ws, wsinfo where user_ws.imei = wsinfo.imei and user_ws.username = %s and wsinfo.simnum = %s', (username, simnum))

def deleteRelationSql(wsdbpool, username, imei):
    return wsdbpool.runOperation('delete from user_ws where username = %s and imei = %s', (username, imei))

def selectDefaultRelationSql(wsdbpool, username):
    return wsdbpool.runQuery('select * from user_ws where username = %s and isdefault = "1"', (username,))

def updateStickNameSql(wsdbpool, username, imei, name):
    wsdbpool.runOperation('update user_ws set name = %s where username = %s and imei = %s', (name, username, imei))




def insertSosnumberSql(wsdbpool, imei, sosnumber, contact):
    return wsdbpool.runOperation('replace into sosnumber (imei, sosnumber, contact) values(%s, %s, %s)', (imei, sosnumber, contact))

def selectSosnumberSql(wsdbpool, imei):
    return wsdbpool.runQuery('select * from sosnumber where imei = %s', (imei,))

def deleteSosnumberSql(wsdbpool, imei, sosnumber):
    return wsdbpool.runOperation('delete from sosnumber where imei = %s and sosnumber = %s', (imei, sosnumber))


def checkSosnumberSql(wsdbpool, imei, sosnumber):
    return wsdbpool.runQuery('select * from sosnumber where imei = %s and sosnumber = %s', (imei, sosnumber))



def insertLocationSql(wsdbpool, imei, longitude, latitude, timestamp):
    return wsdbpool.runOperation('replace into location (imei, longitude, latitude, timestamp) values (%s, %s, %s, %s)', (imei, float(longitude), float(latitude), timestamp))

def selectWsinfoSql(wsdbpool, imei):
    return wsdbpool.runQuery('select * from wsinfo where imei = %s', (imei,))

def updateWsinfoPwdSql(wsdbpool, imei, adminpwd):
    return wsdbpool.runOperation('update wsinfo set adminpwd = %s where imei = %s', (adminpwd, imei))

def selectWsinfoBySimnum(wsdbpool, simnum):
    return wsdbpool.runQuery('select * from wsinfo where simnum = %s', (simnum,))


def insertWsinfoSql(wsdbpool, imei, imsi = None, simnum = None, adminpwd='123456'):
    return wsdbpool.runOperation('replace into wsinfo (imei, imsi, simnum, adminpwd) values (%s, %s, %s, %s)', (imei, imsi, simnum, adminpwd))

def selectLocationSql(wsdbpool, imei, timestamp):
    return wsdbpool.runQuery('select imei, longitude, latitude, unix_timestamp(timestamp) from location where imei = %s and unix_timestamp(timestamp) > %s', (imei, timestamp[0:-3]))




def insertTempRelationSql(wsdbpool, simnum, username, name):
    return wsdbpool.runOperation('replace into temp_user_ws (simnum, username, name) values( %s, %s, %s)', (simnum, username, name))

def deleteTempRelationSql(wsdbpool, simnum):
    return wsdbpool.runOperation('delete from temp_user_ws where simnum = %s', (simnum,))

def selectTempRelationSql(wsdbpool, simnum):
    return wsdbpool.runQuery('select * from temp_user_ws where simnum = %s', (simnum,))




def insertTempSosSql(wsdbpool, imei, sosnumber, contact):
    return wsdbpool.runOperation('replace into temp_sos (imei, sosnumber, contact) values(%s, %s, %s)', (imei, sosnumber, contact))

def selectTempSosSql(wsdbpool, imei, sosnumber):
    return wsdbpool.runQuery('select * from temp_sos where imei = %s and sosnumber = %s', (imei, sosnumber))

def deleteTempSosSql(wsdbpool, imei, sosnumber):
    return wsdbpool.runOperation('delete from temp_sos where imei = %s and sosnumber = %s', (imei, sosnumber))


  

if __name__ == '__main__':

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

    import sys
    from sqlPool import wsdbpool
    #wsdbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456', unix_socket='/tmp/mysql.sock')
    #wsdbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456')
    print createTableSql(wsdbpool).addCallbacks(onSuccess, onError)

    '''
    payload = dict()
    payload['username'] = 'superman'
    payload['sticks'] = list()
    payload['sticks'].append({'name': 'alice', 'imei': '1024'})
    payload['sticks'].append({'name': 'bob', 'imei': '2012'})
    payload['sticks'].append({'name': 'cathy', 'imei': '2048'})

    handleUploadSql(wsdbpool, payload).addCallbacks(onSuccess, onError)



    selectRelationSql(wsdbpool, 'alice').addCallback(testResult).addErrback(testResult)
    handleBindSql(wsdbpool, '1,2046,asdflkj,15652963154').addCallback(onSuccess).addErrback(onError)
    selectUserSql(wsdbpool, 'batman').addCallback(testResult).addErrback(testResult)
    insertLocationSql(wsdbpool, '4321', '23.1298733', '12.1198712', '20151010120012').addCallback(onSuccess).addErrback(onError)
    if sys.argv[1] == 'insert':
        insertTempSosSql(wsdbpool, '1024', '+8615652963154', '超人').addCallback(testResult).addErrback(testResult)
    elif sys.argv[1] == 'delete':
        deleteTempSosSql(wsdbpool, '1024', '+8615652963154').addCallback(testResult).addErrback(testResult)
    else:

    insertTempRelationSql(wsdbpool, '15652963154', 'alice').addCallback(testResult).addErrback(testResult)
    selectTempRelationSql(wsdbpool, '15652963154').addCallback(testResult).addErrback(testResult)
    deleteTempRelationSql(wsdbpool, '15652963154').addCallback(testResult).addErrback(testResult)
    deleteSosnumberSql(wsdbpool, '1024', '+8615652963154', ).addCallback(testResult).addErrback(testResult)
    deleteRelationSql(wsdbpool, 'alice', '0').addCallback(testResult).addErrback(testResult)
    insertRelationSql(wsdbpool, 'alice', '3', 'batman').addCallback(testResult).addErrback(testResult)
    selectSosnumberSql(wsdbpool, '1024').addCallback(testUtf).addErrback(testResult)
    insertSosnumberSql(wsdbpool, '1024', '+8615652963154', '超人').addCallback(testResult).addErrback(testResult)
    getLocationSql(wsdbpool, '4321', '1400000000000').addCallback(testResult).addErrback(testResult)
    insertWsinfoSql(wsdbpool, '1984').addCallback(testResult).addErrback(testResult)
    selectWsinfoSql(wsdbpool, '1984').addCallback(testResult).addErrback(testResult)
    selectLocationSql(wsdbpool, '4321', '1400000000').addCallback(testResult).addErrback(testResult)
    '''
    reactor.run()
