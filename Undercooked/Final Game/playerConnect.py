import socket
from socket import AF_INET, SOCK_DGRAM

ipServer = '172.20.10.6'

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Parse the position and IP address String. Returns a list.
def parseData(data):
    parsed = data.split(',')
    return parsed

while True:
    init_msg = "Hello"
    client.sendto(init_msg.encode(),(ipServer,8080))