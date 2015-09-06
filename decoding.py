from struct import pack, unpack
FROM_SERVER_TAG = '\x55'
FROM_DEVICE_TAG = '\xaa'

URGENT = '\x01'
NOT_URGENT = '\x01'

MESSAGE = "I have a good breakfast"

def getLength(MESSAGE):
    return pack('!h', (len(MESSAGE)))


number = '\x15\x65\x29\x63\x15\x4f\xff\xff'

def getPhoneNoFromHex(number):
    from binascii import b2a_hex
    return b2a_hex(number)[0:11]

def getMessage(rawMsg):
    return rawMsg[14:-1]


