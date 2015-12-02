# -*- coding:utf-8 -*-
from twisted.enterprise import adbapi

wsdbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456', cp_reconnect=True)
#bsdbpool = adbapi.ConnectionPool("MySQLdb", db="bsdb", user='tanghao', passwd='123456', cp_reconnect=True)
#wsdbpool = adbapi.ConnectionPool("MySQLdb", db="wsdb", user='tanghao', passwd='123456', unix_socket='/tmp/mysql.sock', cp_reconnect=True)
