# -*- coding:utf-8 -*-
from sqlhelper import *

def getMessage(rawMsg):
    return rawMsg[14:-1]

def insertLocation(message):
    
    message = message.split(',')
    print message
    imei = str(message[1]).strip()
    timestamp = '20'+ message[2].strip()
    longitude = message[3][:-1].strip()
    latitude = message[4][:-1].strip()
    if (message[3][-1] == 'W') or (message[3][-1] == 'w'):
        longitude = '-' + longitude
    if (message[4][-1] == 's') or (message[4][-1] == 'S'):
        latitude = '-' + latitude
    if insertLocationSql(imei, longitude, latitude,  timestamp):
        return "Result:3,1"
    else:
        return "Result:3,0"

def insertSos(message):
    message = message.split(',')
    print "IMEI: %s\nPhone: %s" % (message[1], message[2])
    return "Result:2,1"

def checkImsi(message):
    message = message.split(',')
    print "IMEI: %s\nIMSI: %s" % (message[1], message[2])
    return "Result:4,1"

def startBind(message):
    message = message.split(',')
    print "IMEI: %s\nCHECKSUM: %s\nNUMBER: %s" % (message[1], message[2], message[3])
    return "Result:1,1"





if __name__ == '__main__':
    location = '3, 123456789abcedf0, 150930141223, 23.12321W, 87.22N'
    sos = '2, 123456789abcedf0, +150930141223'
    imsi = '2, 123456789abcedf0, 123150930141223'
    print checkImsi(imsi)
