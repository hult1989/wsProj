# -*- coding:utf-8 -*-
import mysql.connector
import time
from twisted.internet import reactor, defer
from twisted.enterprise import adbapi
from twisted.python import failure
import random
from appException import *

SQLUSER = 'tanghao'
PASSWORD = '123456'

def handleUnsubscribeSql(wsdbpool, username, imei):
    return wsdbpool.runInteraction(_handleUnsubscribe, username, imei)

def _handleUnsubscribe(txn, username, imei):
    txn.execute('select * from userinfo where username = %s', (username,))
    if len(txn.fetchall()) == 0:
        raise NoUserException
    txn.execute('select * from wsinfo where imei = %s', (imei,))
    if len(txn.fetchall()) == 0:
        raise NoImeiException
    txn.execute('select * from user_ws where username = %s and imei = %s', (username, imei))
    if len(txn.fetchall()) == 0:
        raise NoSubException
    return txn.execute('delete from user_ws where username = %s and imei = %s', (username, imei))



def handleRegisterandUploadSql(wsdbpool, payload):
    return wsdbpool.runInteraction(_handleRegisterUpload, payload)

def _handleRegisterUpload(txn, payload):
    #check if user already exists
    txn.execute('select * from userinfo where username = %s', (str(payload['username']),))
    if len(txn.fetchall()) != 0:
        return 400
    # register
    txn.execute('replace into userinfo (username, password, date) values(%s, %s, curdate())', (payload['username'], payload['password']))

    #if app do upload after register
    if 'sticks' in payload:
        for stick in payload['sticks']:
            txn.execute('replace into user_ws (username, imei, name, isdefault, state) values (%s, %s, %s, "0", "s")', (payload['username'], stick['imei'], stick['name']))
        txn.execute('replace into user_ws (username, imei, name, isdefault, state) values (%s, %s, %s, "1", "s")', (payload['username'], payload['sticks'][-1]['imei'], payload['sticks'][-1]['name']))
    return True


def handleSubscribeByCodeSql(wsdbpool, payload):
    return wsdbpool.runInteraction(_handleSubscribeByCode, payload)

def _handleSubscribeByCode(txn, payload):
    imei = _getImeiByCode(txn, payload['code'])
    if imei == 0:
        return 0
    print 'code is: ', payload['code'], 'imei is: ', imei
    #user didn't regist before and just want to get imei
    txn.execute('select simnum from wsinfo where imei = %s', (imei,))
    simnum = txn.fetchall()[0][0]
    print 'simnum is: ', simnum
    if 'username' in payload:
        txn.execute('update user_ws set isdefault = 0 and state = "s" where username = %s', (str(payload['username']),))
        txn.execute('replace into user_ws(username, imei, name, isdefault, state) values(%s, %s, %s, 1, "s")', (str(payload['username']), imei, str(payload['name'])))
    return (str(imei), str(simnum))




def insertBsLocationSql(bsdbpool, mcc, mnc, lac, cid, longitude, latitude):
    return bsdbpool.runInteraction(_insertBsLocation, mcc, mnc, lac, cid, longitude, latitude)

def _insertBsLocation(txn, mcc, mnc, lac, cid, longitude, latitude):
    tableName = 'mcc' + str(mcc) + 'mnc' + str(mnc)
    txn.execute('insert into ' + tableName + ' (lac, cid, longitude, latitude, date) values(%s, %s, %s, %s, curdate())', (lac, cid, float(longitude), float(latitude)))
    return True


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
    #1,123456789abcdef,bon13800000000,+8613600000000
    message = message.split(',')
    imei = message[1]
    simnum = message[2][3:]
    userphone = message[3]

    #check if stick has already accepted bind request from app by sms 
    txn.execute('select username, name from temp_user_ws where simnum = %s', (simnum,))
    result = txn.fetchall()
    if len(result) == 0:
        return False

    #stick did receive bind request from app
    username = result[0][0]
    name = result[0][1]
    #get user's phone number from his sms, which was sent to stick
    txn.execute('update userinfo set phone = %s where username = %s', (userphone, username))

    #new bind stick will be set as default
    txn.execute('update user_ws set isdefault = 0 where username = %s', (username,))

    #if the user is the first to bind the stick, he will be set as the owner of the stick
    txn.execute('select state from user_ws where imei = %s', (imei,))
    if len(txn.fetchall()) == 0:
        #stick has never been bond before
        txn.execute('replace into user_ws (username, imei, name, isdefault, state) values (%s, %s, %s, "1", "o")', (username, imei, name))
    else:
        txn.execute('select state from user_ws where username = %s and imei = %s', (username, imei))
        result = txn.fetchall()
        if len(result) == 0:
            #stick has been bound, but not by this user
            txn.execute('replace into user_ws (username, imei, name, isdefault, state) values (%s, %s, %s, "1", "b")', (username, imei, name))
            #this stick has been bond by this user
        elif result[0][0] == 's':
            txn.execute('update user_ws set state = "b" where username = %s and imei = %s', (username, imei))

    txn.execute('delete from temp_user_ws where simnum = %s', (simnum,))
    txn.execute('update wsinfo set simnum = %s, adminpwd = "123456" where imei = %s', (simnum, imei))
    return True


def handleSyncSosSql(wsdbpool, message):
    return wsdbpool.runInteraction(_handlleSyncSos, message)

def _handlleSyncSos(txn, message):
    #5,123456789abcdef,3,7,+8613800000000,+8613800000001,+8613800000002
    message = message.split(',')
    imei = message[1]
    numbersInStick = list()
    for number in message[4:]:
        if len(number) != 0:
            numbersInStick.append(number)
            txn.execute('select contact from temp_sos where imei = %s and sosnumber = %s', (imei, number))
            contact = txn.fetchall()
            if len(contact) != 0:
                #this number is both in temp_sos and in message5 from stick, it means that this number shoulde be added to the sosnumber table
                txn.execute('replace into sosnumber (imei, sosnumber, contact) values(%s, %s, %s)', (imei, number, contact[0][0]))
                txn.execute('delete from temp_sos where imei = %s and sosnumber = %s', (imei, number))

    txn.execute('select sosnumber from sosnumber where imei = %s', (imei,))
    numbersInDbEntries = txn.fetchall()
    for numberEntry in numbersInDbEntries:
        if numberEntry[0] not in numbersInStick:
            #the number exists in server but not in the message from the stick, it means that this number shoule be deleted
            txn.execute('delete from sosnumber where imei = %s and sosnumber = %s', (imei, numberEntry[0]))
            txn.execute('delete from temp_sos where imei = %s and sosnumber = %s', (imei, numberEntry[0]))
    return True



def handleSosSql(wsdbpool, message):
    return wsdbpool.runInteraction(_handleSos, message)

def _handleSos(txn, message):
    #2,123456789abcdef,add13800000000
    message = message.split(',')
    imei = message[1]
    sosnumber = message[2][3:]
    txn.execute('select * from temp_sos where imei = %s and sosnumber = %s', (imei, sosnumber))
    contactentry = txn.fetchall()
    # sosnumber from walkingstick and what from app don't match
    if len(contactentry) == 0:
        return False
    '''
    contactentry = contactentry[0]
    if message[2][0:3] == 'del':
        txn.execute('delete from sosnumber where imei = %s and sosnumber = %s', (imei,sosnumber))
    elif message[2][0:3] == 'add':
        txn.execute('replace into sosnumber (imei, sosnumber, contact) values (%s, %s, %s)', (contactentry[0], contactentry[1], contactentry[2]))

    txn.execute('delete from temp_sos where imei = %s and sosnumber = %s', (imei, sosnumber))
    '''
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
        #check if relation between user and stick has be established before
        txn.execute('select * from user_ws where username = %s and imei = %s', (payload['username'], stick['imei']))
        if len(txn.fetchall()) == 0:
            txn.execute('replace into user_ws (username, imei, name, isdefault, state) values (%s, %s, %s, "0", "s")', (payload['username'], stick['imei'], stick['name']))
        txn.execute('replace into user_ws (username, imei, name, isdefault, state) values (%s, %s, %s, "1", "s")', (payload['username'], payload['sticks'][-1]['imei'], payload['sticks'][-1]['name']))
    return True


def selectRelationByImeiSql(wsdbpool, username, imei):
    return wsdbpool.runQuery('select * from user_ws where username = %s and imei =%s', (username, imei))

def selectRelationSql(wsdbpool, username):
    return wsdbpool.runQuery('select  wsinfo.imei, user_ws.name, wsinfo.simnum, user_ws.state from user_ws, wsinfo where user_ws.imei = wsinfo.imei and user_ws.username = %s', (username,))


def selectRelationByUsernameSimnumSql(wsdbpool, username, simnum):
    return wsdbpool.runQuery('select wsinfo.imei, user_ws.state from user_ws, wsinfo where user_ws.imei = wsinfo.imei and user_ws.username = %s and wsinfo.simnum = %s', (username, simnum))

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

def deleteAllSosSql(wsdbpool, imei):
    return wsdbpool.runOperation('delete from sosnumber where imei = %s', (imei,))

def checkSosnumberSql(wsdbpool, imei, sosnumber):
    return wsdbpool.runInteraction(_checkSosnumber, imei, sosnumber)

def _checkSosnumber(txn, imei, sosnumber):
    txn.execute('select * from sosnumber where imei = %s and sosnumber = %s', (imei, sosnumber))
    return txn.fetchall()
    

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
    return wsdbpool.runInteraction(_insertTempSos, imei, sosnumber, contact)

def _insertTempSos(txn, imei, sosnumber, contact):
    txn.execute('select * from sosnumber where imei = %s', (imei,))
    if len(txn.fetchall()) >= 3:
        return '507'
    else:
        txn.execute('replace into temp_sos (imei, sosnumber, contact) values(%s, %s, %s)', (imei, sosnumber, contact))

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
        print failure.value.errCode
        reactor.stop()

    import sys
    from sqlPool import wsdbpool, bsdbpool
    #wsdbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456', unix_socket='/tmp/mysql.sock')
    #wsdbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456')
    selectRelationSql(wsdbpool, 'zox').addCallbacks(onSuccess, onError)

    reactor.run()
