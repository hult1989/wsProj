# -*- coding:utf-8 -*-
from wsbasic import *
from sqlhelper import *
from json import dumps, loads

'''
def insertLocation(payload):
    if insertLocationSql(Location(imei = payload['imei'], longitude=payload['longitude'], latitude=payload['latitude'], timestamp='20'+payload['timestamp'])):
        return '1'
    return '0'
'''

def getLocation(imei, timestamp):
    if isImeiExistSql(imei) == False:
        return '403'
    locations = getLocationSql(imei, timestamp)
    if len(locations) == 0:
        return '504'
    return dumps({'result': '1', 'locations': locations})


if __name__ == '__main__':
    '''
    l = Location('1024', '123.1231', '232.332', '150930110900')
    payload = dict(vars(l))
    insertLocation(payload)
    '''
    print getLocation('15652963154', '1042067880000')
