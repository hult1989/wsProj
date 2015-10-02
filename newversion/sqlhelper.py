# -*- coding:utf-8 -*-
import mysql.connector
from wsbasic import *
import time
from twisted.internet import reactor
from twisted.enterprise import adbapi

SQLUSER = 'tanghao'
PASSWORD = '123456'


def insertUserSql(dbpool, username, passwd, phone=None, email=None):
    return dbpool.runOperation('replace into userinfo (username, password, phone, email, date) values (%s, %s, %s, %s, CURDATE())', (username, passwd, phone, email))

def selectUserSql(dbpool, username):
    return dbpool.runQuery('select * from userinfo where username = %s', (username,))





def insertRelationSql(dbpool, username, imei, name, isdefault='1'):
    return dbpool.runOperation('replace into user_ws (username, imei, name, isdefault) values(%s, %s, %s, %s)', (username, imei, name, isdefault))

def selectRelationSql(dbpool, username):
    return dbpool.runQuery('select * from user_ws where username = %s', (username,))

def deleteRelationSql(dbpool, username, imei):
    return dbpool.runOperation('delete from user_ws where username = %s and imei = %s', (username, imei))




def insertSosnumberSql(dbpool, imei, sosnumber, contact):
    return dbpool.runOperation('replace into sosnumber (imei, sosnumber, contact) values(%s, %s, %s)', (imei, sosnumber, contact))

def selectSosnumberSql(dbpool, imei):
    return dbpool.runQuery('select * from sosnumber where imei = %s', (imei,))

def deleteSosnumberSql(dbpool, imei, sosnumber):
    return dbpool.runOperation('delete from sosnumber where imei = %s and sosnumber = %s', (imei, sosnumber))




def insertLocationSql(dbpool, imei, longitude, latitude, timestamp):
    return dbpool.runOperation('replace into location (imei, longitude, latitude, timestamp) values (%s, %s, %s, %s)', (imei, float(longitude), float(latitude), timestamp))

def selectWsinfoSql(dbpool, imei):
    return dbpool.runQuery('select * from wsinfo where imei = %s', (imei,))




def insertWsinfoSql(dbpool, imei, imsi = None, simnum = None, adminpwd='123456'):
    return dbpool.runOperation('replace into wsinfo (imei, imsi, simnum, adminpwd) values (%s, %s, %s, %s)', (imei, imsi, simnum, adminpwd))
    
def selectLocationSql(dbpool, imei, timestamp):
    return dbpool.runQuery('select imei, longitude, latitude, unix_timestamp(timestamp) from location where imei = %s and unix_timestamp(timestamp) > %s', (imei, timestamp[0:-3]))

    '''
    print type(values)
    locations = []
    for v in values:
        locations.append({'imei': str(v[0]), 'longitude': str(float(v[1])), 'latitude': str(float(v[2])), 'timestamp': str(v[3])+'000' })
    return locations
    '''
   
def testResult(result):
    print result
    reactor.stop()

def testUtf(result):
    for r in result:
        for i  in r:
            print i
    reactor.stop()


if __name__ == '__main__':
    dbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456')
    selectUserSql(dbpool, 'batman').addCallback(testResult).addErrback(testResult)
    '''
    #deleteSosnumberSql(dbpool, '1024', '+8615652963154', ).addCallback(testResult).addErrback(testResult)
    #deleteRelationSql(dbpool, 'alice', '0').addCallback(testResult).addErrback(testResult)
    #insertRelationSql(dbpool, 'alice', '3', 'batman').addCallback(testResult).addErrback(testResult)
    selectRelationSql(dbpool, 'alice').addCallback(testResult).addErrback(testResult)
    selectSosnumberSql(dbpool, '1024').addCallback(testUtf).addErrback(testResult)
    insertSosnumberSql(dbpool, '1024', '+8615652963154', '超人').addCallback(testResult).addErrback(testResult)
    insertLocationSql(dbpool, '4321', '23.1298733', '12.1198712', '20151010120012').addCallback(testResult).addErrback(testResult)
    getLocationSql(dbpool, '4321', '1400000000000').addCallback(testResult).addErrback(testResult)
    insertWsinfoSql(dbpool, '1984').addCallback(testResult).addErrback(testResult)
    selectWsinfoSql(dbpool, '1984').addCallback(testResult).addErrback(testResult)
    selectLocationSql(dbpool, '4321', '1400000000').addCallback(testResult).addErrback(testResult)
    '''
    reactor.run()
