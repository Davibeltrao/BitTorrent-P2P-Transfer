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
		seq = pack("!L", self.numSeq)
		key = message.encode()
		finalMessage = messageType + seq + key
		sent = self.con.sendto(finalMessage, self.servAdress)
		self.receiveKeyData(messageType, self.numSeq, key)

	def receiveKeyData(self, messageType, seqEsperado, key):
		flagRetransmissao = False
		self.con.settimeout(4)
		try:
			data, adress = self.con.recvfrom(414)
			seq = unpack("!L", data[2:6])[0]
			if seq != seqEsperado:
				print("Mensagem incorreta do ", adress)
			else:
				print(adress, " has the key ", data[6:].decode())
		except:
			print("Retrasmiting Data....")
			flagRetransmissao = True
		finally:
			if flagRetransmissao == True:
				self.numSeq = self.numSeq + 1
				seq = pack("!L", self.numSeq)
				finalMessage = messageType + seq + key
				sent = self.con.sendto(finalMessage, self.servAdress)
				try:
					data, adress = self.con.recvfrom(414)
					seq = unpack("!L", data[2:6])[0]
					if seq != self.numSeq or seq != seqEsperado + 1:
						print("Mensagem incorreta do ", adress)
					else:
						print(adress, " has the key ", data[6:].decode())
				except:
					print("\nNENHUMA RESPOSTA RECEBIDA\n")
					self.numSeq = self.numSeq + 1
					return
				finally:
			#		print("Terminei retransmissao")
					pass
			try:
				while True:
					data, adress = self.con.recvfrom(414)
					seq = unpack("!L", data[2:6])[0]
					if seq != seqEsperado:
						print("Mensagem incorreta do ", adress)
					else:
						print(adress, " has the key ", data[6:].decode())
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
			print(adress, " <=Topology=> ", data[6:].decode())
		except:
			print("Retrasmiting Data....")
			flagRetransmissao = True
		finally:
			if flagRetransmissao == True:
				self.numSeq = self.numSeq + 1
				seq = pack("!L", self.numSeq)
				finalMessage = messageType + seq
				sent = self.con.sendto(finalMessage, self.servAdress)
				try:
					data, adress = self.con.recvfrom(414)
					seq = unpack("!L", data[2:6])[0]
					if seq != self.numSeq or seq != seqEsperado + 1:
						print("Mensagem incorreta do ", adress)
					else:
						print(adress, " <=Topology=> ", data[6:].decode())		
				except:
					print("\nNENHUMA RESPOSTA RECEBIDA\n")
					self.numSeq = self.numSeq + 1
					return
				finally:
					#print("Terminei retransmissao")
					pass
			try:
				while True:
					data, adress = self.con.recvfrom(414)
					seq = unpack("!L", data[2:6])[0]
					if seq != seqEsperado and flagRetransmissao == False:
						print("Mensagem incorreta do ", adress)
					else:
						print(adress, " <=Topology=> ", data[6:].decode())
			except:
				print("No more data")
			self.numSeq = self.numSeq + 1


	def quit(self):
		self.con.close()

	def loop(self):
		while True:
			print('==============================================')
			print('   	     O QUE DESEJA FAZER ?')
			print('    ?  + chave = Consulta por uma chave')
			print('    T          = Consulta a topologia da rede')
			print('    Q          = Terminar')
			print('==============================================')
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