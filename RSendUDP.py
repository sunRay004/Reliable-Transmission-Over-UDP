from collections import namedtuple
import socket
import sys

# constant values
MTU = 10 #bytes
MAX_HEADER_SIZE = 4 #bytes

adress = "127.0.0.1"
port = 12345

DATA_SIZE = MTU - MAX_HEADER_SIZE

# sending to server via udp
# sock.sendto(str.encode("fuck"),("127.0.0.1",12345))
# sock.sendto(str.encode("eeeee"),("127.0.0.1",12345))

# get file
# split file into packets
# make list of packets
# add header info to packets (+ is ack)
#     packet sent will have seqence + data, stored should have sequence + data + is acked?
#
# enter loop:
# send packets across sliding window
# scan for recieved acknolagements
# ?need to track what is in window

for i in range(len(sys.argv)):
    if i == 1:
        adress = sys.argv[i]
    if i == 2:
        port = int(sys.argv[i])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


file = open("testtext.txt", "r")
filedata = file.read().encode()

packet = namedtuple("packet", ['seq' ,'data','ack'])
packets: list[packet] = []

for x in range(0,len(filedata)//DATA_SIZE +1):
    pak = packet(seq=x, data=filedata[x*DATA_SIZE:x*DATA_SIZE+DATA_SIZE],ack=False)
    # filedata[x*DATA_SIZE:x*DATA_SIZE+DATA_SIZE]
    # x,filedata[x*DATA_SIZE:x*DATA_SIZE+DATA_SIZE], False
    packets.append(pak)

for x in packets:
    payload = int(x.seq).to_bytes(MAX_HEADER_SIZE, byteorder="big", signed=True) + x.data
    print("sending packet {} with data {} \n".format(x.seq,x.data))
    sock.sendto(payload,(adress,port))

sock.sendto((-len(packets)).to_bytes(MAX_HEADER_SIZE, byteorder="big", signed=True),(adress,port))