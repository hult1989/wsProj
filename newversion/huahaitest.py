# -*- coding:utf-8 -*-
import sys
import socket
from sys import argv
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8081)
sock.connect(server_address)
f = open('./test.log', 'w')


def testTcp(message):
    try:
	sock.sendall(message)
        data = sock.recv(96)
        print >> sys.stderr, 'received "%s"' % data
    finally:
	print >>sys.stderr, 'closing socket'
	sock.close()



if __name__ == '__main__':
    message = ''
     
    location = '3,123456789abcedf0,150930141223,23.12321W,87.22234N'
    addsos = '2,2046,+15882205392'
    delsos = '2,2046,-15882205392'
    imsi = '4,123456789abcedf0,123150930141223'
    bind = '1,123456789abcedf0,123150930141223,15882205392'

    if argv[1] == 'addsos':
        testTcp(addsos)
    if argv[1] == 'delsos':
        testTcp(delsos)
    elif argv[1] == 'location':
        testTcp(location)
    elif argv[1] == 'imsi':
        testTcp(imsi)
    elif argv[1] == 'bind':
        testTcp(bind)

