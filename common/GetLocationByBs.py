# -*- coding:utf-8 -*-
import urllib2, urllib
from gcj2wgs import transform

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
    locations = urllib2.urlopen(request).read()
    locations = eval(locations)['result']['location'].split(',')
    result = transform(float(locations[1]), float(locations[0]))
    return str(result[0])+','+str(result[1])

