import math
import socket
import sys
import time
import Test

# constant values
MTU = 20 #bytes
MAX_HEADER_SIZE = 4 #bytes
WINDOW_SIZE = 200 #bytes
TIMEOUT = 1 #seconds

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

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock = Test.sok()

file = open("testtext.txt", "r")
filedata = file.read().encode()

#packet = {'seq': 0,'data' : None, 'ack' : False, 'exp' : 0} # 'seq' ,'data', 'ack', 'exp'
packets: list[list] = []

for x in range(0,math.ceil(len(filedata)/DATA_SIZE)):
    pak = [x,filedata[x*DATA_SIZE:x*DATA_SIZE+DATA_SIZE],False,0.0]    # 'seq' ,'data', 'ack', 'exp'
    # filedata[x*DATA_SIZE:x*DATA_SIZE+DATA_SIZE]
    # x,filedata[x*DATA_SIZE:x*DATA_SIZE+DATA_SIZE], False
    packets.append(pak)

traveling = 0 # not num of packets, but amount of mtus that are out, bytes
sock.setblocking(False)
curlen = len(packets)
packets.append([-curlen,b'',False,0.0])
acked = 0

while True:   # sending + ack loop
    # payload = int(x.seq).to_bytes(MAX_HEADER_SIZE, byteorder="big", signed=True) + x.data
    # print("sending packet {} with data {} \n".format(x.seq,x.data))
    # sock.sendto(payload,(adress,port))

    for x in packets:   # 0'seq'int , 1'data'bytes, 2'ack'bool, 3'exp'float
            # if first time being sent, there is space in window and not acknowlaged OR
            # if not first time being sent, and not acknowlaged
        if (((x[3] == 0) and (traveling <= WINDOW_SIZE - MTU) and (x[2] == False)) or ((x[3] < time.time()) and ((x[3] != 0)) and (x[2] == False))):    # packet should be sent, and fits in window
                # if sent for first time, increment traveling
            if(x[3] == 0):
                traveling = traveling + MTU

            x[3] = time.time() + TIMEOUT  # set new timeout
            print("time is {}, packet {} timeout at {}".format(time.time(), x[0], x[3]))
            payload = int(x[0]).to_bytes(MAX_HEADER_SIZE, byteorder="big", signed=True) + x[1]
            sock.sendto(payload,(adress,port))
            print("sent packet number {} with data {}, total bytes in flight is {} \n".format(x[0],x[1],traveling))
        
        # else:
        #     # if not (x[3] < time.time()):
        #     #     print("r: not expired")
        #     # if not (traveling <= WINDOW_SIZE - MTU):
        #     #     print("r: window size")
        #     # if not (x[2] == False):
        #     #     print("r: acknowlaged")
        #     pass
    

    try: 
        acknowlagement = int.from_bytes(sock.recv(MTU), byteorder="big", signed=True)  # ack = seq, no data
        if(acknowlagement < 0):
            acknowlagement = -acknowlagement
        if(packets[acknowlagement][2] == False):
            packets[acknowlagement][2] = True
            traveling = traveling - MTU
            acked = acked + 1
            print("acknowlaged packet number {}, total bytes in flight is {}, total acked {} \n".format(acknowlagement, traveling, acked))
        else:
            print("Duplicate ack recieved")
    except BlockingIOError: 
        pass
    except Exception:
        print("Connection was closed by the peer \n")
        print("acked {}, non acked {}, message length = {}".format(acked,traveling/MTU,len(packets)))
        break
            

    if(acked == len(packets)):
        print("done, all packets acknowlaged")
        sock.close()
        break


