import pprint
import socket
import sys
from struct import pack, unpack

class Servent:

	def __init__(self, address):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.con.bind(address)
		self.servent_port = address[1]
		self.keyDict = {}
		self._neighbors = []
		self.visited = False
		self.listOfSeqNums = []

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
		print( type(msgSeq))
		print( type(msgTipo))
		print (type(msgTtl))
		print (type(msgPorto))
		print (type(msgInfo))
		msg = msgTipo+msgTtl+msgSeq+ipOrigem+msgPorto+msgInfo
		for neighbor in self._neighbors:
			try:
				(addr, port) = neighbor
				self.con.sendto(msg, (addr, int(port)))
			except Exception as e:
				print("Dude where's my neighbor?")

	def keyReq(self, data, address):
		numSeq = unpack("!L", data[2:6])[0]
		if (address, numSeq) in self.listOfSeqNums:
			print("Already received this message.")
			return True
		self.listOfSeqNums.append((address, numSeq))
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
			return False
		except Exception as e:
			print("Key Doesnt exist here")
			return False

	def topoFlood(self, key, numSeq, ttl, ipOrigem, portoOrigem, address0, address1):
		msgSeq = pack('!L', numSeq)
		#print("SEQUENCIA  = ", numSeq)
		msgTipo = pack('!H', 8)
		msgTtl = pack('!H', ttl)
		#msgIp = pack('!B', int(ipOrigem[0])) + pack('!B', int(ipOrigem[1])) + pack('!B', int(ipOrigem[2])) + pack('!B', int(ipOrigem[3])) 
		msgPorto = pack('!H', portoOrigem)
		msgInfo = key
		fim_info = ""
		msg = msgTipo+msgTtl+msgSeq+ipOrigem+msgPorto+msgInfo
		print("INFO DA MENSAGEM = ", msgInfo.decode())
		for neighbor in self._neighbors:
			try:
				(addr, port) = neighbor
				fim_info = addr.encode() + ":".encode() + str(port).encode() + " ".encode()
				#fim_info = ""
				print("FIM MENSAGEM = ", fim_info)
				#msg = msg + fim_info
				self.con.sendto(msg + fim_info, (addr, int(port)))
			except Exception as e:
				print("Dude where's my neighbor?")

	def topoReq(self, data, address, info, address_cliente, porta, flag_frist = False):
		#Porta = Porta do servidor atual

		seq = unpack("!L", data[2:6])[0]
		if (address_cliente, seq) in self.listOfSeqNums:
			print("Already received this message.")
			return True
		self.listOfSeqNums.append((address_cliente, seq))
		resp = pack("!H", 9)
		seqResp = pack("!L", seq)
		print("ADDRESS SEND = ", address_cliente)
		finalMessage = resp + seqResp + info
		print("INFO = ", info)
		if flag_frist == True:
			finalMessage = finalMessage + address[0].encode() + ":".encode() + str(self.servent_port).encode() + " ".encode()
		sent = self.con.sendto(finalMessage, address_cliente)	
		return False


	def loop(self):
		while True:
			data, address = self.con.recvfrom(414)
			typeMessage = unpack("!H", data[:2])[0]
			print("TYPE = ", typeMessage)
			print("DATA = ", data)
			print("FROM = ", address)
			if typeMessage == 5:
				msgNumSeq = unpack('!L', data[2:6])[0]
				achouChave = self.keyReq(data, address)
				if achouChave==True:
					continue # Talvez retirar, pra continuar as iteracoes
				ip, port = address
				msgIp = pack('!B', int(ip.split('.')[0])) + pack('!B', int(ip.split('.')[1])) + pack('!B', int(ip.split('.')[2])) + pack('!B', int(ip.split('.')[3])) 
				self.keyFlood(data[6:], msgNumSeq, 3, msgIp, port)
			elif typeMessage == 6:
				flag_frist = True
				info_inicial = "".encode()
				ip, port = address
				msgIp = pack('!B', int(ip.split('.')[0])) + pack('!B', int(ip.split('.')[1])) + pack('!B', int(ip.split('.')[2])) + pack('!B', int(ip.split('.')[3])) 
				msgNumSeq = unpack('!L', data[2:6])[0]
				jaRecebeu = self.topoReq(data, address, info_inicial, address, self.servent_port, flag_frist)
				if jaRecebeu==True:
					continue
				data = data + address[0].encode() + ":".encode() + str(self.servent_port).encode() + " ".encode()
				print("Dados = ", data[6:].decode())
				self.topoFlood(data[6:], msgNumSeq, 3, msgIp, port, address[0], self.servent_port)
			elif typeMessage==7:
				msgTtl = unpack('!H', data[2:4])[0]
				if msgTtl<=0:
					continue
				msgNumSeq = unpack('!L', data[4:8])[0]
				msgIpOrig = unpack('!L', data[8:12])[0]
				msgPort = unpack('!H', data[12:14])[0]				#enviar resposta
				
				teste = socket.inet_ntoa(data[8:12])
				
				print("SERA MANO??? = ", teste)
				#codigo do keyReq() nao funciona?
				#ipStr = str(unpack('!B', data[8])[0])+'.'+str(unpack('!B', data[9])[0])+'.'+str(unpack('!B', data[10])[0])+'.'+str(unpack('!B', data[11])[0])
				addr = (teste, int(msgPort))
				achouChave = self.keyReq((b'00'+data[4:8]+data[14:]), addr)
				if achouChave==True:
					continue # Acho q tem q tirar esse continue, pra continuar as iteracoes
				if int(msgTtl)==1:
					continue
				self.keyFlood(data[14:], msgNumSeq, int(msgTtl)-1, data[8:12], msgPort)
			elif typeMessage==8:
				msgTtl = unpack('!H', data[2:4])[0]
				if msgTtl<=0:
					continue
				msgNumSeq = unpack('!L', data[4:8])[0]
				msgIpOrig = unpack('!L', data[8:12])[0]
				msgPort = unpack('!H', data[12:14])[0]
				ip, port = address
				print("IP ORIG = ", msgIpOrig)

				teste = socket.inet_ntoa(data[8:12])

				address_cliente = (teste, msgPort)
				print("CLIENTE AD = ", address_cliente)
				self.topoReq(data[2:], address, data[14:], address_cliente, self.servent_port)
				msgIp = pack('!B', int(ip.split('.')[0])) + pack('!B', int(ip.split('.')[1])) + pack('!B', int(ip.split('.')[2])) + pack('!B', int(ip.split('.')[3])) 
				#print("INFO = ", info)
				if int(msgTtl)==1:
					continue
				self.topoFlood(data[14:], msgNumSeq, int(msgTtl)-1, msgIp, msgPort, address[0], self.servent_port)
				continue
			elif typeMessage == 9:
				print("RECEBI DADOS dados = ", data[6:])

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
	print('Neighbors:')
	pprint.pprint(servent.getNeighbors())
	servent.loop()
