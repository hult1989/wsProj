from sqlwriter import insertLocation 
from walkingstickbasic import *
from decoding import getPhoneNoFromHex, getMessage
import time

def processData(data):
    userid = getPhoneNoFromHex(data[1:9])
    #print userid
    gpsInfo = getMessage(data)
    gpsInfo = gpsInfo.split(',')
    #print gpsInfo
    location = UserLocation(userid, float(gpsInfo[0]), float(gpsInfo[1]), str(int(time.time())))
    #print vars(location)
    insertLocation(location)
    return True




data = '\x55' 
data = data + '\x15\x69\x25\x63\x15\x4f\xff\xff'
data = data + '\x55' * 5
data = data + '88.112, 100.223'

