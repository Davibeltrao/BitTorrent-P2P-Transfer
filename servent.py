import socket
import sys


class Servent:

	def __init__(self, Adress):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.con.bind(Adress)

# Bind the socket to the port
print >>sys.stderr, 'starting up on %s port %s' % server_address
while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data, address = sock.recvfrom(4096)
    
    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >>sys.stderr, data
    
    if data:
        sent = sock.sendto(data, address)
        print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)


if __name__ == "__main__":
	PORT = int(sys.argv[1])
	ADRESS = ("", PORT)
	servidor = Servent(ADRESS)