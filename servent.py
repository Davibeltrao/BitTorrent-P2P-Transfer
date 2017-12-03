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
		#msgIp = pack('!B', int(ipOrigem[0])) + pack('!B', int(ipOrigem[1])) + pack('!B', int(ipOrigem[2])) + pack('!B', int(ipOrigem[3])) 
		msgPorto = pack('!H', portoOrigem)
		msgInfo = key
		msg = msgTipo+msgTtl+msgSeq+str(ipOrigem)+msgPorto+msgInfo
		for neighbor in self._neighbors:
			try:
				(addr, port) = neighbor
				self.con.sendto(msg, (addr, int(port)))
			except Exception as e:
				print("Dude where's my neighbor?")

	def keyReq(self, data, address):
		numSeq = unpack("!L", data[2:6])[0]
		requestedKey = data[6:].decode()
		requestedKey = requestedKey.replace('\n', '')
		print("REQ = ", requestedKey, " & NumSeq = ", numSeq)
		try:
			resp = pack("!H", 9)
			seqResp = pack("!L", numSeq)
			keyResp = self.keyDict[requestedKey]
			message = keyResp.encode()
			finalMessage = resp + seqResp + message
			sent = self.con.sendto(finalMessage, address)
			print("SENT = ", sent)
			return True
		except Exception as e:
			print("Key Doesnt exist here")
			return False

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
			if typeMessage == 5:
				msgNumSeq = unpack('!L', data[2:6])[0]
				achouChave = self.keyReq(data, address)
				if achouChave==True:
					continue
				ip, port = address
				msgIp = pack('!B', int(ip.split('.')[0])) + pack('!B', int(ip.split('.')[1])) + pack('!B', int(ip.split('.')[2])) + pack('!B', int(ip.split('.')[3])) 
				self.keyFlood(data[6:], msgNumSeq, 3, msgIp, port)
			elif typeMessage == 6:
				self.topoReq(data, address)
			elif typeMessage==7:
				msgTtl = unpack('!H', data[2:4])[0]
				if msgTtl<=0:
					continue
				msgNumSeq = unpack('!L', data[4:8])[0]
				msgIpOrig = unpack('!L', data[8:12])[0]
				msgPort = unpack('!H', data[12:14])[0]				#enviar resposta
				#codigo do keyReq() nao funciona?
				ipStr = str(unpack('!B', data[8])[0])+'.'+str(unpack('!B', data[9])[0])+'.'+str(unpack('!B', data[10])[0])+'.'+str(unpack('!B', data[11])[0])
				addr = (ipStr, int(msgPort))
				achouChave = self.keyReq((b'00'+data[4:8]+data[14:]), addr)
				if achouChave==True:
					continue
				self.keyFlood(data[14:], msgNumSeq, int(msgTtl)-1, msgIpOrig, msgPort)
			elif typeMessage==8:
				msgTtl = unpack('!H', data[2:4])[0]
				if msgTtl<=0:
					continue
				msgNumSeq = unpack('!L', data[4:8])[0]
				msgIpOrig = unpack('!L', data[8:12])[0]
				msgPort = unpack('!H', data[12:14])[0]
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
