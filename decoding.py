from struct import pack, unpack
from binascii import b2a_hex
FROM_SERVER_TAG = '\x55'
FROM_DEVICE_TAG = '\xaa'

URGENT = '\x01'
NOT_URGENT = '\x01'

MESSAGE = "I have a good breakfast"

def getLength(MESSAGE):
    return pack('!h', (len(MESSAGE)))

message = '\x55'
message = message + '\x15\x65\x29\x63\x15\x4f\xff\xff'
message = message + '\x55' * 5
message = message +  '\x15\x09\x01\x17\x41\x2311395720132W0198452138s'
message = message + '\x55'


def getPhoneNoFromRaw(rawMsg):
    return b2a_hex(rawMsg[1:9])[0:11]

def getMessage(rawMsg):
    '''message means payload, including timestamp and gps info, without checksum'''
    return rawMsg[14:-1]

def getTimeFromMessage(message):
    timestamp = message[0:6]
    return '20' + b2a_hex(timestamp)

def getLongitudeFromMessage(message):
    longitude = float(message[6:17]) / 1e8
    if message[17] == 'e' or message[17] == 'E':
        longitude = longitude 
    elif message[17] == 'w' or message[17] == 'W':
        longitude = -longitude
    return longitude
    

def getLatitudeFromMessage(message):
    latitude = float(message[18:-1]) / 1e8
    if message[-1] == 'N' or message[-1] == 'n':
        latitude = latitude
    elif message[-1] == 's' or message[-1] == 'S':
        latitude = -latitude
    return latitude

def createReturnValue(rawMsg, isSuccess):
    response = rawMsg[0:11]
    response += '\x21'
    response += rawMsg[12:14]
    if isSuccess:
        response += '0'
    else:
        response += '1'
    response += getMessage(rawMsg)
    response += rawMsg[-1]
    return response
    


if __name__ == '__main__':
    rawMsg = message
    print getPhoneNoFromRaw(rawMsg)
    message = getMessage(message)
    print message
    print getTimeFromMessage(message)
    print getLongitudeFromMessage(message)
    print getLatitudeFromMessage(message)
    print rawMsg
    print createReturnValue(rawMsg, True)
