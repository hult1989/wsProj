# -*- coding:utf-8 -*-
import time, math
from twisted.python import log, failure
from twisted.internet import protocol, reactor, defer, threads, task
from twisted.protocols import basic
from twisted.enterprise import adbapi
from twisted.web.client import Agent, readBody, HTTPConnectionPool

from sqlhelper import handleSosSql, handleBindSql, insertLocationSql, handleImsiSql, selectWsinfoSql, insertBatteryLevel
from SosModuleSql import deleteSosNumberSql, syncSosSql, syncFamilySql
from StickModuleSql import handleStickBindAck
from GetLocationByBs import getLocationByBsinfo, getLocationByBsinfoAsync, _httpBodyToGpsinfo, getLocationFromMinigpsAsync, decodeMinigpsResult 
from OnlineStatusHelper import onlineStatusHelper
from GpsMessage import GpsMessageOldVer, GpsMessage


SQLUSER = 'tanghao'
PASSWORD = '123456'

def insertLocation(httpagent, wsdbpool, message):
    def _getGpsinfoCallback(wsinfo, imei, lac, cid, signal, timestamp):
        try:
            imsi = wsinfo[0][1]
            mcc = imsi[0:3]
            mnc = imsi[3:5]
            #return threads.deferToThread(getLocationByBsinfo, mcc, mnc, imei, imsi, lac, cid, signal, timestamp)
            return getLocationByBsinfoAsync(httpagent, mcc, mnc, imei, imsi, lac, cid, signal).addCallback(readBody).addCallback(_httpBodyToGpsinfo, (mcc, mnc, imei, imsi, lac, cid, signal))
        except Exception as e:
            d = defer.Deferred()
            if len(wsinfo) == 0:
                d.errback(failure.Failure(Exception('cannot read imsi of the simcard in this stick' )))
            else:
                d.errback(failure.Failure(e))
            return d

    def _insertLocation(gpsinfo, wsdbpool, imei, timestamp, issleep):
        if gpsinfo != '0,0':
            gpsinfo = str(gpsinfo).split(',')
            return insertLocationSql(wsdbpool, imei, gpsinfo[0], gpsinfo[1], timestamp, issleep, 'b')
        else:
            d = defer.Deferred()
            d.callback(failure.Failure(Exception('illegal result, cannot get gpsinfo by bsinfo ')))
            return d


    '''
    message = message.split(',')
    imei = str(message[1]).strip()
    if int(message[2].strip()) == 0:
        timestamp = time.strftime('%Y%m%d%H%M%S', time.gmtime(time.time()))
    else:
        timestamp = '20'+ message[2].strip()

    longitude, latitude = _getGpsinfoFromMessage(message)

    #get longitude and latitude in string format form message
    lac = int(message[5], 16)
    cid = int(message[6], 16)
    signal = _convertSignalToRssi(int(message[7]))
    try:
        batteryLevel = int(message[8])
        charging = int(message[9])
        issleep = message[10]
    except Exception as e:
        batteryLevel = 50
        charging = 0
        issleep = '0'
    '''
    if message[0] == '3':
        #old format
        gpsMsg = GpsMessageOldVer(message)
        if gpsMsg.longitude == 0 or gpsMsg.latitude == 0:
            d = selectWsinfoSql(wsdbpool, gpsMsg.imei).addCallback(_getGpsinfoCallback, gpsMsg.imei, gpsMsg.baseStationInfo.lac, gpsMsg.baseStationInfo.cid, gpsMsg.baseStationInfo.signal, gpsMsg.timestamp).addCallback(_insertLocation, wsdbpool, gpsMsg.imei, gpsMsg.timestamp, gpsMsg.issleep)
        else:
            d = insertLocationSql(wsdbpool, gpsMsg.imei, gpsMsg.longitude, gpsMsg.latitude,  gpsMsg.timestamp, gpsMsg.issleep)

    elif message[0] == 'a':
        #new format
        gpsMsg = GpsMessage(message)
        if gpsMsg.longitude == 0 or gpsMsg.latitude == 0:
            d = getLocationFromMinigpsAsync(httpagent, gpsMsg.mcc, gpsMsg.mnc, gpsMsg.baseStationInfos).addCallback(readBody).addCallback(decodeMinigpsResult, (gpsMsg.mcc, gpsMsg.mnc, gpsMsg.baseStationInfos)).addCallback(_insertLocation, wsdbpool, gpsMsg.imei, gpsMsg.timestamp, gpsMsg.issleep)
        else:
            d = insertLocationSql(wsdbpool, gpsMsg.imei, gpsMsg.longitude, gpsMsg.latitude,  gpsMsg.timestamp, gpsMsg.issleep)

    #same operation for both old format msg and new format msg
    d.addCallback(insertBatteryLevel, wsdbpool, gpsMsg.imei, gpsMsg.batteryLevel, gpsMsg.charging, gpsMsg.timestamp)
    return d

def onError(failure, transport, message):
    log.msg('RECV %s from %s, RESP WITH %s, because of %s' %(message, str(transport.client), ''.join(("Result:", message[0], ',0')), str(failure.value)))
    transport.write(''.join(("Result:", message[0], ',0'))+'\r\n')

def onGpsMsgError(failure, message, transport):
    log.msg('RECV %s from %s, RESP WITH %s, because of %s' %(message, str(transport.client), ''.join(("Result:", message[0], ',0')), str(failure.value)))
    log.msg(message)

def onGpsMsgSuccess(result, message):
    log.msg(message + ' processing finished')



class WsServer(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory
    
    def onSuccess(self, result, transport, message):
        if result == True or result == None or type(result) == tuple or type(result) == list:
            transport.write(''.join(("Result:", message[0], ',1'))+'\r\n')
	    log.msg('RECV %s  from %s, RESP WITH %s' %(message, str(transport.client), ''.join(("Result:", message[0], ',1'))))
        elif result == False:
	    log.msg('RECV %s , RESP WITH %s' %(message, ''.join(("Result:", message[0], ',0'))))
            transport.write(''.join(("Result:", message[0], ',0'))+'\r\n')

    def connectionMade(self):
        log.msg('transport %s connected' %(str(self.transport.client)))


    def lineReceived(self, message):
        log.msg('%s send message %s' %(str(self.transport.client), message))
        message = message.strip()
        if not message:
            return
        imei = message.split(',')[1]
        self.factory.onlineHelper.updateOnlineStatus(imei, self.transport)

        for m in message.split(','):
            if len(m) == 0 and message[0] != '5' and message[0] != '7':
                self.transport.write(''.join(("Result:", message[0], ',0'))+'\r\n')
	        log.msg('RECV %s , RESP WITH %s' %(message, ''.join(("Result:", message[0], ',0'))))
                return

        #this is ok becase protocol is instantiated for each connection, so it won't has confusion
        if message[0] == '1':
            handleStickBindAck(self.factory.wsdbpool, message).addCallbacks(self.onSuccess, onError, callbackArgs=(self.transport, message), errbackArgs=(self.transport, message))
        elif message[0] == '2':
            handleSosSql(self.factory.wsdbpool, message).addCallbacks(self.onSuccess, onError, callbackArgs=(self.transport, message), errbackArgs=(self.transport, message))
        elif message[0] in ('3', 'a'):
            imei = message.split(',')[1]
            if message[0] == '3':
                self.transport.write(''.join(("Result:", message[0], ',1'))+'\r\n')
            elif message[0] == 'a':
                status = self.factory.onlineHelper.connectedSticks[imei]
                if not status.getAppRequestTime():
                    self.transport.write(''.join(("Result:", message[0], ',1,0'))+'\r\n')
                else:
                    log.msg('resp with app request time %s' %(status.getAppRequestTime()))
                    self.transport.write(''.join(("Result:", message[0], ',1,',time.strftime('%Y%m%d%H%M%S', time.gmtime(status.getAppRequestTime()))[2:]))+'\r\n')

	    #log.msg('RECV %s , RESP WITH %s' %(message, ''.join(("Result:", message[0], ',1'))))
            try:
                tempList = list()
                for msg in message.splitlines():
                    #d = insertLocation(self.factory.wsdbpool, msg).addCallbacks(self.onSuccess, onError, callbackArgs=(self.transport, msg), errbackArgs=(self.transport, msg))
                    tempList.append(insertLocation(self.factory.httpagent, self.factory.wsdbpool, msg))
                d = defer.gatherResults(tempList, consumeErrors=True).addCallbacks(onGpsMsgSuccess, onGpsMsgError, callbackArgs=(msg,), errbackArgs=(msg, self.transport))
            except Exception as e:
                onGpsMsgError(failure.Failure(Exception(e)), message, self.transport)

        elif message[0] == '4':
            handleImsiSql(self.factory.wsdbpool, message).addCallbacks(self.onSuccess, onError, callbackArgs=(self.transport, message), errbackArgs=(self.transport, message))
        elif message[0] == '5':
            syncSosSql(self.factory.wsdbpool, message).addCallbacks(self.onSuccess, onError, callbackArgs=(self.transport, message), errbackArgs=(self.transport, message))
        elif message[0] == '6':
            if message[-2:] == 'ok' or message[-2:] == 'OK':
                deleteSosNumberSql(self.factory.wsdbpool, message.split(',')[1]).addCallbacks(self.onSuccess, onError, callbackArgs=(self.transport, message), errbackArgs=(self.transport, message))
            else:
                self.transport.write(''.join(("Result:", message[0], ',0'))+'\r\n')
	        log.msg('RECV %s , RESP WITH %s' %(message, ''.join(("Result:", message[0], ',0'))))
        elif message[0] == '7':
            syncFamilySql(self.factory.wsdbpool, message).addCallbacks(self.onSuccess, onError, callbackArgs=(self.transport, message), errbackArgs=(self.transport, message))

        elif message[0] == '9':
	    log.msg('RECV %s , RESP WITH %s' %(message, ''.join(("Result:", message[0], ',1'))))
            self.transport.write(''.join(("Result:", message[0], ',1'))+'\r\n')


        elif message[0] == 'R':
            message =  message.split(',')
            status = onlineStatusHelper.connectedSticks[message[-1]]
            d = status.getDefer()
            if d and not d.called:
                if message[1] == '1':
                    log.msg('确认打开gps')
                    status.gpsStatus = True
                else:
                    log.msg('确认关闭gps')
                    status.gpsStatus = False
                d.callback(True)
            log.msg(str(vars(status)))




class WsServerFactory(protocol.Factory):
    def __init__(self, wsdbpool):
        self.wsdbpool = wsdbpool
        self.onlineHelper = onlineStatusHelper
        self.httpagent = Agent(reactor, pool=HTTPConnectionPool(reactor))
        self.onlineHelper.getLoopingKickStart()
        '''
        self.cctask = task.LoopingCall(self.onlineHelper.kickoutIdleConnection)
        self.cctask.start(60)
        '''

        

    def buildProtocol(self, addr):
        return WsServer(self)


if __name__ == '__main__':
    from sqlPool import wsdbpool
    from sys import stdout
    #wsdbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456')
    log.startLogging(stdout)
    reactor.listenTCP(8081, WsServerFactory(wsdbpool))
    reactor.run()
    '''
    def _convertToFloat(lati_or_longi):
        #convert string to float, iiff.ffff->dd + (ffffff)/60
        index = lati_or_longi.index('.')
        lati_or_longi_intPart = int(lati_or_longi[0:index-2])
        lati_or_longi_floatPart = float(lati_or_longi[index-2:]) / 60
        return lati_or_longi_intPart + lati_or_longi_floatPart

    def _getGpsinfoFromMessage(message):
        longitude = message[3][:-1].strip()
        latitude = message[4][:-1].strip()
        longitude = _convertToFloat(longitude)
        latitude = _convertToFloat(latitude)
        if longitude == 0 or latitude == 0:
            return 0, 0
        if (message[3][-1] == 'W') or (message[3][-1] == 'w'):
            longitude = 0 - longitude
        if (message[4][-1] == 's') or (message[4][-1] == 'S'):
            latitude = 0 - latitude
        return longitude, latitude

    def _convertSignalToRssi(signal):
        if signal < 4 or signal == 99:
            return -107
        elif signal < 10:
            return -93
        elif signal < 16:
            return -71
        elif signal < 22:
            return -69
        elif signal < 28:
            return -57
        elif signal >= 28:
            return -56

'''

