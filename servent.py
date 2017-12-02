import pprint
import socket
import sys
from struct import pack, unpack

class Servent:

	def __init__(self, address):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.con.bind(address)
		self.keyDict = {}
		self._neighbors = []

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

	def addNeighbor(self, arg3):
		address = arg3.split(':')
		self._neighbors.append((address[0], address[1]))

	def getNeighbors(self):
		listOfNeighbors = []
		for neighbor in self._neighbors:
			listOfNeighbors.append(neighbor)
		return listOfNeighbors

	def keyFlood(self, key, numSeq, ttl, ipOrigem, portoOrigem):
		msgSeq = pack('!L', numSeq)
		msgTipo = pack('!H', 7)
		msgTtl = pack('!H', ttl)
		msgIp = pack('!L', ipOrigem)
		msgPorto = pack('!L', portoOrigem)
		msgInfo = key
		msg = msgTipo+msgSeq+msgIp+msgPorto+msgInfo
		for neighbor in this._neighbors:
			try:
				(addr, port) = neighbor.split(':')
				self.con.sendto(msg, (addr, int(port)))
			except:
				print("Dude where's my neighbor?")

	def keyReq(self, data, address):
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
			sent = self.con.sendto(finalMessage, address)
			print("SENT = ", sent)
		except:
			print("Key Doesnt exist here")

	def topoFlood(self):
		return

	def topoReq(self, data, address):
		print("ENTREI")
		seq = unpack("!L", data[2:6])[0]
		for key, value in self.keyDict.items():
			print("Key = ", key, " & Value = ", value)
	
		resp = pack("!H", 9)
		seqResp = pack("!L", seq)
		finalMessage = resp + seqResp
		for key, value in self.keyDict.items():
			finalMessage = finalMessage + key.encode()
		sent = self.con.sendto(finalMessage, address)	

	def loop(self):
		while True:
			data, address = self.con.recvfrom(414)
			typeMessage = unpack("!H", data[:2])[0]
			print("TYPE = ", typeMessage)
			print(type(typeMessage))
			if typeMessage == 5:
				msgNumSeq = unpack('!L', data[3:7])
				self.keyReq(data, address)
				ip, port = address
				self.keyFlood(msgKey, msgNumSeq, 3, ip, port)
			elif typeMessage == 6:
				self.topoReq(data, address)
			elif typeMessage==7:
				msgTtl = unpack('!H', data[2:4])
				if msgTtl<=0:
					continue
				msgNumSeq = unpack('!L', data[4:8])
				msgIpOrig = unpack('!L', data[8:12])
				msgPort = unpack('!L', data[12:14])
				#enviar resposta
				#codigo do keyReq() nao funciona?
				for neighbor in listOfNeighbors:
					(addr, port) = neighbor.split(':')
					address = (addr, int(port))
					keyReq(b'00'+data[4:8]+data[14:], address)
				self.keyFlood(data[14:], msgNumSeq, msgTtl, msgIpOrig, msgPort)
			elif typeMessage==8:
				msgTtl = unpack('!H', data[2:4])
				if msgTtl<=0:
					continue
				msgNumSeq = unpack('!L', data[4:8])
				msgIpOrig = unpack('!L', data[8:12])
				msgPort = unpack('!L', data[12:14])
				continue

#Bind the socket to the port
# while True:
#     print(sys.stderr, '\nwaiting to receive message')
#     data, address = sock.recvfrom(414)
#     if data:
#         sent = sock.sendto(data, address)
#         print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)


if __name__ == "__main__":
	PORT = int(sys.argv[1])
	address = ("", PORT)
	servent = Servent(address)
	servent.setDict(sys.argv[2])
	for neighbor in sys.argv[3:13]:
		servent.addNeighbor(neighbor)
	print 'Neighbors:'
	pprint.pprint(servent.getNeighbors())
	servent.loop()
