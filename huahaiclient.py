import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('huahai', 8081)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
	message = '\x55'
        message = message + '\x15\x65\x29\x63\x15\x4f\xff\xff'
        message = message + '\x55' * 5
        message = message +  '\x55\x20\xff\xff\x15\x09\x01\x17\x41\x231139572012W019845218s'
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
