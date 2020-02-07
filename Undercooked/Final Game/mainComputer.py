import numpy as np
import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv.bind(('172.20.10.6', 8080))

#Currently an infinite loop just in case the test goes wrong
while True:
    #Receive String of "position,IP address" from Clients
    data, addr = serv.recvfrom(4096)
    if not data: break
    data = data.decode()
    print("Data provided is: ")
    print(data)
    print('\n')
