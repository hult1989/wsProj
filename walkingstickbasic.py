import copy
class User:
    def __init__(self, username, password, phone, userid=None):
        #time means craeted date and time
        self.username = username
        self.phone = phone
        self.password = password
        self.userid = userid


class UserLocation:
    def __init__(self, userid, longitude, latitude, timestamp):
        self.userid = userid
        self.longitude = longitude
        self.latitude = latitude
        self.timestamp = timestamp


class SOSNumberList:
    def __init__(self,  userid, numbers):
        self.userid = userid
        self.numbers = copy.copy(numbers)

class LocationData:
    def __init__(self, electronicFenceID, longitude, latitude):
        self.electronicFenceID = electronicFenceID
        self.longitude = longitude
        self.latitude = latitude

class ElectronicFence:
    def __init__(userid, locationList, date):
        self.userid = userid
        self.locationList = copy.copy(locationList)
        self.date = date

class VersionInfo:
    def __init__(userid, deviceVID, devicePID, deviceSN, appVID, appPID, appIMEI):
        userid = userid
        self.deviceVID = deviceVID
        self.devicePID = devicePID
        self.deviceSN = deviceSN
        self.appVID = appVID
        self.appPID = appPID
        self.appIMEI = appIMEI
        
