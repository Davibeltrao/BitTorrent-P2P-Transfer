import socket
import sys

class Cliente:
	
	def __init__(self, Adress):
		self.con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.serv_adress = Adress

	def loop(self):
		



if __name__ == "__main__":
	adress = sys.argv[1]
	adress = adress.split(":")
	IP =  adress[0]
	PORT = int(adress[1])
	connection_address = (IP, PORT)
	cliente = Cliente(adress)