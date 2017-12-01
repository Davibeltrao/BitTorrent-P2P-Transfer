import socket
import sys


class Servent:

	def __init__(self, Adress):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.con.bind(Adress)
		self.keyDict = {}
		self.neighbors = {}

	def setDict(self, file):
		with open(file, 'r') as f:
			for i in f:
				c = i.split()
				#print(c[0])
				if(c[0] == "#"):
					continue
				if c[0] not in self.keyDict:
					self.keyDict[c[0]] = c[1]
				else:
					self.keyDict[c[0]] = c[1]
			f.close()
		print("RTMP = ", self.keyDict["rtmp"])
		print("TCP MUX = ", self.keyDict["tcpmux"])
		print("NBP = ", self.keyDict["nbp"])
		print("COMPRESSNET = ", self.keyDict["compressnet"])

	def loop(self):
		while True:
			data, adress = self.con.recvfrom(414)			
			pass


#Bind the socket to the port
# while True:
#     print(sys.stderr, '\nwaiting to receive message')
#     data, address = sock.recvfrom(414)
#     if data:
#         sent = sock.sendto(data, address)
#         print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)


if __name__ == "__main__":
	PORT = int(sys.argv[1])
	ADRESS = ("", PORT)
	servent = Servent(ADRESS)
	servent.setDict(sys.argv[2])
	servent.loop()
