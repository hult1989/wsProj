from struct import pack, unpack
from binascii import b2a_hex
FROM_SERVER_TAG = '\x55'
FROM_DEVICE_TAG = '\xaa'

URGENT = '\x01'
NOT_URGENT = '\x01'

MESSAGE = "I have a good breakfast"

def getLength(MESSAGE):
    return pack('!h', (len(MESSAGE)))


number = '\x15\x65\x29\x63\x15\x4f\xff\xff'
message = '\x55\x20\xff\xff\x15\x09\x01\x17\x41\x231139572012W019845218s'

def getPhoneNoFromHex(number):
    return b2a_hex(number)[0:11]

def getMessage(rawMsg):
    return rawMsg[14:-1]

def getTimeFromMessage(message):
    timestamp = message[4:10]
    return '20' + b2a_hex(timestamp)

def getLongitudeFromMessage(message):
    longitude = float(message[10:20]) / 1e7
    if message[20] == 'e' or message[20] == 'E':
        longitude = longitude 
    elif message[20] == 'w' or message[20] == 'W':
        longitude = -longitude
    return longitude
    

def getLatitudeFromMessage(message):
    latitude = float(message[21:-1]) / 1e7
    if message[-1] == 'N' or message[-1] == 'n':
        latitude = latitude
    elif message[-1] == 's' or message[-1] == 'S':
        latitude = -latitude
    return latitude
    

if __name__ == '__main__':
    print getTimeFromMessage(message)
    print getLongitudeFromMessage(message)
    print getLatitudeFromMessage(message)
