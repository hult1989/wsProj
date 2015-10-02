# -*- coding:utf-8 -*-
import copy

class User:
    def __init__(self, username, password, phone=None, email=None, userid=None):
        #time means craeted date and time
        self.username = username
        self.password = password
        self.phone = phone
        self.userid = userid
        self.email = email


class Location:
    def __init__(self, imei, longitude, latitude, timestamp):
        self.imei = imei
        self.longitude = longitude
        self.latitude = latitude
        self.timestamp = timestamp

      
