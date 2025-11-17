from collections import namedtuple
import socket
import sys
import Test

MTU = 20 #bytes
MAX_HEADER_SIZE = 4 #bytes

adress = "127.0.0.1"
port = 12345

# recieving message via udp
# sock.bind(("127.0.0.1",12345))
# msg = sock.recv(1028)
# print("fuck recieved: {}".format(msg))

# get packet
# split into header/data
# if out of order fill with nulls
# put packet in [seq]
# fin packet negative, fin seq identifies how much packets we still need.
#     fill array with nulls up to fin seq, then when no nulls left finish
# combine all back into file

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(len(sys.argv)):
    if i == 1:
        adress = sys.argv[i]
    if i == 2:
        port = int(sys.argv[i])

packets: list[str|None] = []

sock = Test.sok()
sock.bind((adress,port))

msgsize = 0
nullcount = 0
returnAdress = None
msgf = []
while True:

    if(msgsize != 0 and nullcount == 0):
        if(msgsize == len(packets) - 1):
            print("DONE")
            print(msgsize)
            print(nullcount)
            print(len(packets))
            break
    
    
    msgf = sock.recvfrom(MTU)   # recieve and get adress


    msg = msgf[0]
    returnAdress = msgf[1]
    
    msgseq = int.from_bytes(msg[:MAX_HEADER_SIZE], byteorder="big", signed=True)
    msgdata = msg[MAX_HEADER_SIZE:MTU].decode()

    print("got seq {} and data {} \n".format(msgseq,msgdata))

    # send ack even if duplicate, ack just msgseq
    sock.sendto(msgseq.to_bytes(MAX_HEADER_SIZE, byteorder="big", signed=True),returnAdress)
    

    if(msgseq < 0):  # fin packet handling
        msgsize = -msgseq
        msgseq = -msgseq # have the below function append extra nulls, data should be empty and will not affect output. after that should break loop

    while msgseq >= len(packets):    # make sure list has enough entries
        packets.append(None)        # msgseq always 1 less then amount of spaces for packets we should have
        nullcount = nullcount + 1

    if(packets[msgseq] == None):    # replace nulls with data, dont replace duplicates 
        packets[msgseq] = msgdata
        nullcount = nullcount - 1
    


print("Final Message: \n")

print("".join(str(packets))) # type: ignore