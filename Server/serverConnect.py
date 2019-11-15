#https://wiki.python.org/moin/UdpCommunication
#https://www.geeksforgeeks.org/socket-programming-python/

import numpy as np
import socket
import fcntl
import struct
serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

iparray = np.empty((1,40,16),dtype=str)

#Test/Demo Purposes
k = 0

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s'.encode(), ifname[:15].encode())
    )[20:24])

ip = get_ip_address('wlan0')
print(ip)

# Assigns a port for the server that listens to clients connecting to this port.
serv.bind((ip, 8080))
while True:
    while True:
        data, addr = serv.recvfrom(4096)
        if not data: break
        data = data.decode()
        print("Data provided is: ")
        print(data)
        print('\n')

        recData = ""

        #Empty the array if the received data is a RESET function
        if(data == "RESET"):
            iparray = np.empty((1,40,16),dtype=str)
            recData = "RESET"

        #Parse the data into position and IP address.
        else:
            posBool = True
            ipBool = True
            pos = ""
            ip = ""
            i = 0
            while posBool:
                if(data[i] == ','):
                    posBool = False
                    i = i+1
                    break
                pos = pos + data[i]
                i = i+1
            
            while ipBool:
                if(i >= len(data)):
                    ipBool = False
                    break
                ip = ip + data[i]
                i = i+1

            #Add the IP address to the array of IP addresses that will later be referenced
            for j in range (0, len(ip)):
                iparray[(0,int(pos)-1)][j] = ip[j]

            recData = pos

        print("iparray[" + str((int(pos)-1)) + "]: ")

        ipAdd = ""

        for l in range (0,len(iparray[0,int(pos)-1])):
            ipAdd = ipAdd + iparray[0,int(pos)-1][l]

        print(ipAdd)
        print('\n')

        k = k + 1

        recData = (recData).encode()

        serv.sendto(recData,(ipAdd,8080))

        if (k > 0):
            break
        
    if (k > 0):
        break

print("Parsing demo completed")

ipArr = []
for k in range (0,len(iparray[0])):
    ipTemp = ""
    for temp in range (0,len(iparray[0,k])):
        ipTemp = ipTemp + iparray[0,k][temp]
    ipArr.append(ipTemp)

#______________________________________________________________________________________________________#
#Code Test

for add in range (0,len(iparray[0])):
    ipAdd = iparray[0,add]
    testStr = "testLED"
    testStr = testStr.encode()
    serv.sendto(testStr,(ipAdd,8080))

    while True:
        while True:
            data, addr = serv.recvfrom(4096)
            if not data: break
            data = data.decode()
            if (data == "testDone"):
                break
        if (data == "testDone"):
                break

#Check if something is wrong (received a "RESET" message)

#______________________________________________________________________________________________________#
#Time Increment

while True:
    for add in range (0,len(iparray[0])):
        ipAdd = iparray[0,add]
        runStr = "runLED"
        runStr = runStr.encode()
        serv.sendto(runStr,(ipAdd,8080))

        while True:
            while True:
                data, addr = serv.recvfrom(4096)
                if not data: break
                data = data.decode()
                if (data == "runDone"):
                    break
            if (data == "runDone"):
                    break