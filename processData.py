from sqlwriter import insertLocation 
from walkingstickbasic import *
from decoding import *
import time

def processData(data):
    userid = getPhoneNoFromRaw(data)
    #print userid
    message = getMessage(data)
    longitude = getLongitudeFromMessage(message)
    latitude = getLatitudeFromMessage(message)
    timestamp = getTimeFromMessage(message)

    #print gpsInfo
    location = UserLocation(userid, longitude, latitude, timestamp)
    print vars(location)
    try:
        insertLocation(location)
        return True
    except:
        return False


