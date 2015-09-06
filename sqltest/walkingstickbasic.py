import copy
class User:
    def __init__(self, username, password, time, id=None):
        #time means craeted date and time
        self.username = username
        self.password = password
        self.time = time
        self.id = id


class UserLocation:
    def __init__(self, userid, longitude, latitude, time, id = None):
        self.userid = userid
        self.longitude = longitude
        self.latitude = latitude
        self.time = time
        self.id = id


class SOSNumberList:
    def __init__(self, id, userid, numbers):
        self.id = id
        self.userid = userid
        self.numbers = copy.copy(numbers)

class LocationData:
    def __init__(self, id, electronicFenceID, longitude, latitude):
        self.id = id
        self.electronicFenceID = electronicFenceID
        self.longitude = longitude
        self.latitude = latitude

class ElectronicFence:
    def __init__(id, userid, locationList, date):
        self.id = id
        self.userid = userid
        self.locationList = copy.copy(locationList)
        self.date = date

class VersionInfo:
    def __init__(id, userid, deviceVID, devicePID, deviceSN, appVID, appPID, appIMEI):
        userid = userid
        self.deviceVID = deviceVID
        self.devicePID = devicePID
        self.deviceSN = deviceSN
        self.appVID = appVID
        self.appPID = appPID
        self.appIMEI = appIMEI
        
