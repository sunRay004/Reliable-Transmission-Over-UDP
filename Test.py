import random
import socket
import typing

# program uses:
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.setblocking(True)
# sock.sendto(payload,(adress,port))
# sock.recv(MTU)
# sock.bind((adress,port))
# sock.recvfrom(MTU)
droprate = 1 # 


class sok:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def setblocking(self, bool):
        self.sock.setblocking(bool)
    
    def sendto(self, payload, _address):
        rng = random.randrange(0,100,1)
        if(rng < droprate):
            print("dropped a packet")
            return
        
        self.sock.sendto(payload,_address)
        return 
    
    def recv(self, amount):
        return self.sock.recv(amount)
    
    def recvfrom(self, amount):
        return self.sock.recvfrom(amount)
    
    def bind(self,_address):
        self.sock.bind(_address)

    def close(self):
        self.sock.close()