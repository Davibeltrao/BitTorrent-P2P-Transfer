import socket
import sys
from struct import pack, unpack

class Cliente:
	
	def __init__(self, Adress):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.servAdress = Adress
		self.numSeq = 1

	def loop(self):
		while True:
			message = sys.stdin.readline()
			print("Mensagem recebida = ", message)
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

	def topologyConsult(self):
		pass

	def keyConsult(self, message):
		print(message)
		messageType = pack("!H", 5)
		seq = pack("!H", self.numSeq)
		key = message.encode()
		finalMessage = messageType + seq + key
		sent = self.con.sendto(finalMessage, self.servAdress)

	def quit(self):
		self.con.close()


if __name__ == "__main__":
	adress = sys.argv[1]
	adress = adress.split(":")
	IP =  adress[0]
	PORT = int(adress[1])
	connection_address = (IP, PORT)
	cliente = Cliente(connection_address)
	cliente.loop()