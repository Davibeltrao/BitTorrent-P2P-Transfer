import socket
import sys

class Cliente:
	
	def __init__(self, Adress):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.serv_adress = Adress
		self.numseq = 1
		
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
				self.keyConsult(message)
			elif message[0] == "T":
				print("TOPOLOGY")
				self.topologyConsult()

	def topologyConsult(self):
		pass

	def keyConsult(self, message):

		pass

	def quit(self):
		self.con.close()


if __name__ == "__main__":
	adress = sys.argv[1]
	adress = adress.split(":")
	IP =  adress[0]
	PORT = int(adress[1])
	connection_address = (IP, PORT)
	cliente = Cliente(adress)
	cliente.loop()