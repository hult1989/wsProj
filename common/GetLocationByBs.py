# -*- coding:utf-8 -*-
import urllib2, urllib
from eviltransform import gcj2wgs_exact
from pprint import pformat
from stringprod import StringProducer
from twisted.web.http_headers import Headers
from twisted.internet import reactor
from twisted.web.client import Agent, HTTPConnectionPool, readBody
from twisted.python import log
import sys

request = urllib2.Request('http://apilocate.amap.com/position')
#secret key of gaode map service
AMAP_SERVICE_KEY = '56f2c85f19dbfae6269363d64d688173'


def getLocationByBsinfo(mcc, mnc, imei, imsi, lac, cid, signal, timestamp):
    paramsDict = dict()
    paramsDict['accesstype'] = '0'
    paramsDict['key'] = AMAP_SERVICE_KEY
    paramsDict['output'] = 'json'
    paramsDict['imei'] = str(imei)
    paramsDict['imsi'] = str(imsi)
    paramsDict['bts'] = ','.join((str(mcc), str(mnc), str(lac), str(cid), str(signal)))
    params = urllib.urlencode(paramsDict)
    request.add_data(params)
    for i in range(3):
        try:
            locations = urllib2.urlopen(request).read()
            locations = eval(locations)['result']['location'].split(',')
            print locations
            result = gcj2wgs_exact(float(locations[1]), float(locations[0]))
            latlog = str(result[1])+','+str(result[0])
        except Exception as e:
            latlog = '0,0'
        else:
            break
    return latlog

def getLocationByBsinfoAsync(httpagent, mcc, mnc, imei, imsi, lac, cid, signal):
    paramsDict = dict()
    paramsDict['accesstype'] = '0'
    paramsDict['key'] = AMAP_SERVICE_KEY
    paramsDict['output'] = 'json'
    paramsDict['imei'] = str(imei)
    paramsDict['imsi'] = str(imsi)
    paramsDict['bts'] = ','.join((str(mcc), str(mnc), str(lac), str(cid), str(signal)))
    params = urllib.urlencode(paramsDict)
    params = StringProducer(params)
    d = httpagent.request('POST', 'http://apilocate.amap.com/position', Headers({}), params)
    return d


def getLocationFromMinigpsAsync(httpagent, mcc, mnc, bsInfos):
    paramsDict = {}
    params = [mcc, mnc]
    for info in bsInfos:
        params += [info.lac, info.cid, info.signal]
    paramsDict['x'] = '-'.join(params)
    paramsDict['p'] = 1
    paramsDict['mt'] = 0
    paramsDict['needaddress'] = 0
    
    d = httpagent.request('GET', 'http://minigps.org/cw?'+urllib.urlencode(paramsDict), Headers({'Connection': ['Keep-Alive']}), None)
    #d = httpagent.request('GET', 'http://minigps.org/cw', Headers({'Connection': ['Keep-Alive']}), StringProducer(urllib.urlencode(paramsDict)))
    return d

def onResult(body):
    try:
        print eval(body)
    except Exception as e:
        print e, body
    reactor.stop()


def onError(failure):
    print failure.value
    reactor.stop()
    


def _httpBodyToGpsinfo(body, args):
    try:
        locations = eval(body)['result']['location'].split(',')
        result = gcj2wgs_exact(float(locations[1]), float(locations[0]))
        latlog = str(result[1])+','+str(result[0])
        log.msg('Reuslt from amap api %s: ' %(str(args) + '   ' +  latlog))
    except Exception as e:
        log.msg('cannot parse response from amapapi because of %s, result from amap is %s' %(str(e), str(body)))
        latlog = '0,0'
    return latlog



if __name__ == '__main__':
    '''
    print getLocationByBsinfo(460, 00,862609000062526,460002606566466, int('2490', 16), int('10f6', 16), -69,20151218074832)
    print getLocationByBsinfo(460, 00,862609000062526,460002606566466, int('2490', 16), int('10f6', 16), -57,20151218074832)
    print getLocationByBsinfo(460, 00,862609000062526,460002606566466, int('2490', 16), int('0e90', 16), -57,20151218074832)
    '''
    from GpsMessage import GpsMessage
    msg = GpsMessage('3,866523028123929,160101120000,11356.3373E,2232.9325N,050,1,1,0,0460,0000,0000,0007,27ba,0df5,0078,27ba,0f53,0068,27ba,0fbf,0082,27ba,0eda,0083,25f0,0e44,0086,27ba,0f1f,0087,27ba,0df4,0090,6')
    agent = Agent(reactor, pool=HTTPConnectionPool(reactor))
    getLocationFromMinigpsAsync(agent, msg.mcc, msg.mnc, msg.baseStationInfos).addCallback(readBody).addCallbacks(onResult, onError)
    reactor.run()
