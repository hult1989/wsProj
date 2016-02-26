import time
import appServerCommon

class GpsMessageBase(object):
    class BaseStationInfo(object):
        def __init__(self, info):
            self.lac, self.cid, self.signal = info

    def correcTimestamp(self):
        self.timestamp = time.strftime('%Y%m%d%H%M%S', time.gmtime(time.time())) \
                if int(self.timestamp) == 0 else '20' + self.timestamp

    def initLongitudeLatitude(self):
        def _convertToFloat(lati_or_longi):
            #convert string to float, iiff.ffff->dd + (ffffff)/60
            index = lati_or_longi.index('.')
            lati_or_longi_intPart = int(lati_or_longi[0:index-2])
            lati_or_longi_floatPart = float(lati_or_longi[index-2:]) / 60
            return lati_or_longi_intPart + lati_or_longi_floatPart
        self.longitude = _convertToFloat(self.longitude[:-1]) * [1,-1][self.longitude[-1] in ['w', 'W']]
        self.latitude = _convertToFloat(self.latitude[:-1]) * [1,-1][self.latitude[-1] in ['s', 'S']]

class GpsMessageOldVer(GpsMessageBase):
    def __convertSignalToRssi(self, signal):
        if signal < 4 or signal == 99:
            return -107
        elif signal < 10:
            return -93
        elif signal < 16:
            return -71
        elif signal < 22:
            return -69
        elif signal < 28:
            return -57
        elif signal >= 28:
            return -56


    def __init__(self, message):
        message = message.strip().split(',')
        self.imei = message[1]
        self.timestamp = message[2]
        self.correcTimestamp()
        self.longitude, self.latitude = message[3:5]
        self.initLongitudeLatitude()
        self.baseStationInfo = self.BaseStationInfo((int(message[5],16), int(message[6],16), self.__convertSignalToRssi(int(message[7]))))
        try:
            self.batteryLevel = int(message[8])
            self.charging = int(message[9])
            self.issleep = int(message[10])
        except Exception as e:
            self.batteryLevel = '50'
            self.charging = '0'
            self.issleep = '0'





class GpsMessage(GpsMessageBase):
    def __init__(self, message):
        message = message.strip().split(',')[1:]
        self.imei, self.timestamp, self.longitude, self.latitude, \
        self.batteryLevel, self.charging, self.issleep, self.rebootcode, \
        self.mcc, self.mnc, self.timeadvance = message[:11]
        self.baseStationInfos = []
        for i in range(int(message[11])):
            info = self.BaseStationInfo(message[12+i*3:12+(1+i)*3])
            info.signal = hex(110-int(info.signal))[2:]
            self.baseStationInfos.append(info)     
        self.mcc = hex(int(self.mcc))[2:]
        self.mnc = hex(int(self.mnc))[2:]
        self.initLongitudeLatitude()
        self.correcTimestamp()


if __name__ == '__main__':
    #msg = GpsMessage('3,866523028123929,160101120000,11356.3373E,2232.9325N,050,1,1,0,0460,0000,0000,0007,27ba,0df5,0078,27ba,0f53,0068,27ba,0fbf,0082,27ba,0eda,0083,25f0,0e44,0086,27ba,0f1f,0087,27ba,0df4,0090,6')
    msg = GpsMessage('a,862609000057781,160226032659,11403.2502E,2236.9187N,065,0,0,4,0460,0000,0255,0006,27ba,0f53,0072,27ba,0f52,0071,27ba,0fc1,0078,27ba,0f20,0079,27ba,0eda,0085,27ba,0df5,0086,9')
    for k, v in vars(msg).items():
        print k, ': ', v
    for info in msg.baseStationInfos:
        print vars(info)
    '''
    oldVer = '3,866523028123929,160224015217,00000.00000,0000.00000,2540,7a8d,31,100,0,0,0,12'
    old = GpsMessageOldVer(oldVer)
    for k, v in vars(old).items():
        print k, ': ', v
    print vars(old.baseStationInfo)
    '''


