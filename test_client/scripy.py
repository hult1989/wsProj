# -*- coding:utf-8 -*-
import os
import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import Deferred, succeed, DeferredList
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.iweb import IBodyProducer
from zope.interface import implements
from json import dumps
import time
from twisted.internet.task import LoopingCall
import socket



f = open('./testinput.txt')


#server_address = ('localhost', 8081)
server_address = ('smartcane.huahailife.com',8081)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
text = f.readline()
while len(text) != 0:
    sock.sendall(text)
    data = sock.recv(96)
    print text, data
    text = f.readline()
sock.close()
f.close()


