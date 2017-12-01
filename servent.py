import socket
import sys
from struct import pack, unpack

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
					self.keyDict[c[0]] = c[1:]
				else:
					self.keyDict[c[0]] = c[1:]
			f.close()
		print("RTMP = ", self.keyDict["rtmp"])
		print("TCP MUX = ", self.keyDict["tcpmux"])
		print("NBP = ", self.keyDict["nbp"])
		print("COMPRESSNET = ", self.keyDict["compressnet"])

	def keyReq(self, data):
		numSeq = unpack("!L", data[2:6])[0]
		print("NumSeq = ", numSeq)
		requestedKey = data[6:].decode()
		print("REQ = ", requestedKey)

	def loop(self):
		while True:
			data, adress = self.con.recvfrom(414)
			#print("DATA = ", data)
			typeMessage = unpack("!H", data[:2])[0]
			print("TYPE = ", typeMessage)
			print(type(typeMessage))
			if typeMessage == 5:
				self.keyReq(data)
			elif typeMessage == 6:
				pass
			elif typeMessage == 7:
				pass
			elif typeMessage == 8:
				pass
			#print("ADRESS = ", adress)
			#print("NEW DATA = ", data2)
			#data = data + pack("!H", 5151)
			self.con.sendto(data, adress)

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
