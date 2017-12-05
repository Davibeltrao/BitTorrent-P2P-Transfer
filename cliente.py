import socket
import sys
from struct import pack, unpack

class Cliente:
	
	def __init__(self, Adress):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.servAdress = Adress
		self.numSeq = 1

	def topologyConsult(self):
		messageType = pack("!H", 6)
		seq = pack("!L", self.numSeq)
		finalMessage = messageType + seq
		sent = self.con.sendto(finalMessage, self.servAdress)
		self.receiveTopologyData(messageType, self.numSeq)

	def keyConsult(self, message):
		print(message)
		messageType = pack("!H", 5)
		print("NumSeq = ", self.numSeq)
		seq = pack("!L", self.numSeq)
		key = message.encode()
		finalMessage = messageType + seq + key
		print("ServAdress = ", self.servAdress)
		sent = self.con.sendto(finalMessage, self.servAdress)
		self.receiveKeyData(messageType, self.numSeq, key)

	def receiveKeyData(self, messageType, seqEsperado, key):
		flagRetransmissao = False
		self.con.settimeout(4)
		try:
			data, adress = self.con.recvfrom(414)
			#Verificar se mensagem é do tipo 9
			seq = unpack("!L", data[2:6])[0]
			if seq != seqEsperado:
				print("Mensagem incorreta do ", adress)
			else:
				print("Data Received = ", data)
		except:
			print("Retrasmiting Data....")
			flagRetransmissao = True
		finally:
			if flagRetransmissao == True:
				self.numSeq = self.numSeq + 1
				print("New NumSeq = ", self.numSeq)
				seq = pack("!L", self.numSeq)
				finalMessage = messageType + seq + key
				sent = self.con.sendto(finalMessage, self.servAdress)
				try:
					data, adress = self.con.recvfrom(414)
					seq = unpack("!L", data[2:6])[0]
					if seq != self.numSeq:
						print("Mensagem incorreta do ", adress)
					else:
						print("Data Received = ", data)
				except:
					print("Nenhuma resposta recebida")
				finally:
					#self.con.settimeout(0)
					print("Terminei retransmissao")
			try:
				while True:
					data, adress = self.con.recvfrom(414)
					seq = unpack("!L", data[2:6])[0]
					if seq != seqEsperado:
						print("Mensagem incorreta do ", adress)
					else:
						print("Data Received = ", data)	
			except:
				print("No more data")
			self.numSeq = self.numSeq + 1


	def receiveTopologyData(self, messageType, seqEsperado):
		flagRetransmissao = False
		self.con.settimeout(4)
		try:
			data, adress = self.con.recvfrom(414)
			seq = unpack("!L", data[2:6])[0]
			if seq != seqEsperado:
				print("Mensagem incorreta do ", adress)
			#print("Data Received = ", data)
			print(adress, " Send = ", data[6:].decode())
		except:
			print("Retrasmiting Data....")
			flagRetransmissao = True
		finally:
			if flagRetransmissao == True:
				self.numSeq = self.numSeq + 1
				print("New NumSeq = ", self.numSeq)
				seq = pack("!L", self.numSeq)
				finalMessage = messageType + seq
				sent = self.con.sendto(finalMessage, self.servAdress)
				try:
					data, adress = self.con.recvfrom(414)
					seq = unpack("!L", data[2:6])[0]
					if seq != self.numSeq:
						print("Mensagem incorreta do ", adress)
						print("Teste = ", data[6:].decode())
					print("Data Received = ", data)
					print("Teste = ", data[6:].decode())
				except:
					print("Nenhuma resposta recebida")
				finally:
					print("Terminei retransmissao")
			try:
				while True:
					data, adress = self.con.recvfrom(414)
					seq = unpack("!L", data[2:6])[0]
					#print("SEQ ESPERADO = ", seqEsperado, " & SEQ = ", seq)
					if seq != seqEsperado and flagRetransmissao == False:
						print("Mensagem incorreta do ", adress)
						#print("Teste = ", data[6:].decode())
					else:
					#	print("Data Received = ", data)	
						print(adress, " Send = ", data[6:].decode())
			except:
				print("No more data")
			self.numSeq = self.numSeq + 1


	def quit(self):
		self.con.close()

	def loop(self):
		while True:
			message = sys.stdin.readline()
			if(message[0] == "Q"):
				print("QUIT")
				self.quit()
				break # Talvez? Con.close() not working
			elif message[0] == "?":
				print("KEY CONSULT")
				message = message[1:]
				message = message.lstrip()
				self.keyConsult(message)
			elif message[0] == "T":
				print("TOPOLOGY")
				self.topologyConsult()


if __name__ == "__main__":
	adress = sys.argv[1]
	adress = adress.split(":")
	IP =  adress[0]
	PORT = int(adress[1])
	connection_address = (IP, PORT)
	cliente = Cliente(connection_address)
	cliente.loop()