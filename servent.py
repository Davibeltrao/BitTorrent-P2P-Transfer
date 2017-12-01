import socket
import sys
from struct import pack, unpack

class Servent:

	def __init__(self, Adress):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.con.bind(Adress)
		self.keyDict = {}
		self.neighbors = []

	def setDict(self, file):
		with open(file, 'r') as f:
			for i in f:
				c = i.split()
				if(c[0] == "#"):
					continue
				if c[0] not in self.keyDict:
					self.keyDict[c[0]] = " ".join(c[1:])
				else:
					self.keyDict[c[0]] = " ".join(c[1:])
			f.close()
		print("RTMP = ", self.keyDict["rtmp"])
		print("TCP MUX = ", self.keyDict["tcpmux"])
		print("NBP = ", self.keyDict["nbp"])
		print("COMPRESSNET = ", self.keyDict["compressnet"])

	def setNeighbors(self, arg3):
		print("\n\n")
		arg3 = arg3.replace('[', ' ')
		arg3 = arg3.replace(']', '')
		arg3 = arg3.split()
		print(arg3)

	def keyReq(self, data, adress):
		numSeq = unpack("!L", data[2:6])[0]
		requestedKey = data[6:].decode()
		requestedKey = requestedKey.replace('\n', '')
		print("REQ = ", requestedKey, " & NumSeq = ", numSeq)
		print("RTMP DICT = ", self.keyDict["rtmp"])
		try:
			resp = pack("!H", 9)
			seqResp = pack("!L", numSeq)
			keyResp = self.keyDict[requestedKey]
			message = keyResp.encode()
			finalMessage = resp + seqResp + message
			sent = self.con.sendto(finalMessage, adress)
			print("SENT = ", sent)
		except:
			print("Key Doesnt exist here")

	def topoReq(self, data, adress):
		print("ENTREI")
		seq = unpack("!L", data[2:6])[0]
		for key, value in self.keyDict.items():
			print("Key = ", key, " & Value = ", value)
	
		resp = pack("!H", 9)
		seqResp = pack("!L", seq)
		finalMessage = resp + seqResp
		for key, value in self.keyDict.items():
			finalMessage = finalMessage + key.encode()
		sent = self.con.sendto(finalMessage, adress)	

	def loop(self):
		while True:
			data, adress = self.con.recvfrom(414)
			typeMessage = unpack("!H", data[:2])[0]
			print("TYPE = ", typeMessage)
			print(type(typeMessage))
			if typeMessage == 5:
				self.keyReq(data, adress)
			elif typeMessage == 6:
				self.topoReq(data, adress)

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
	servent.setNeighbors(sys.argv[3])
	servent.loop()
