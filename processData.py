from sqlwriter import insertLocation 
from walkingstickbasic import *
from decoding import *
import time

def processData(data):
    userid = getPhoneNoFromHex(data[1:9])
    #print userid
    message = getMessage(data)
    longitude = getLongitudeFromMessage(message)
    latitude = getLatitudeFromMessage(message)
    timestamp = getTimeFromMessage(message)

    #print gpsInfo
    location = UserLocation(userid, longitude, latitude, timestamp)
    #print vars(location)
    insertLocation(location)
    return True


