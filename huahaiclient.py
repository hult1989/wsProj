import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('huahai', 8081)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
	message = '\x55'
        message = message + '\x15\x65\x29\x63\x15\x4f\xff\xff'
        message = message + '\x55' * 5
        d = time.localtime().tm_yday
        h = time.localtime().tm_hour
        m = time.localtime().tm_min
        s = time.localtime().tm_sec
        message = message + '%s.%s, %s.%s' % (str(d), str(h), str(m), str(s))
        message = message + '\x55'
	print >> sys.stderr, 'sending "%s"' % message
	sock.sendall(message)
	amount_received = 0
	amount_expected = len(message)
	
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data
finally:
	print >>sys.stderr, 'closing socket'
	sock.close()
