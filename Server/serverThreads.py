#https://wiki.python.org/moin/UdpCommunication
#https://www.geeksforgeeks.org/socket-programming-python/

import numpy as np
import socket
import socket.timeout as TimeoutException
import fcntl
import struct
serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

maxStudents = 84
maxTime = 1000
ipArr = np.empty(maxStudents,dtype=str)
done = False

#Gets IP address of server so others can connect (should be known by everyone beforehand)
def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s'.encode(), ifname[:15].encode())
        )[20:24])

#Parse the position and IP address String
def parseIP(data):
    iparray = np.empty((1,16),dtype=str)
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
        iparray[0,j] = ip[j]

    ipTemp = ""
    for temp in range (0,len(iparray[0])):
        ipTemp = ipTemp + iparray[0,temp]

    parsed = [pos,ipTemp]
    return parsed

def updateIP(pos,ipAddress):
    ipArr[pos] = ipAddress
    return

def sendMess(message,ipAddress):
    serv.sendto(message,(ipAddress,8080))
    return

#Thread 1
while True:
    while True:
        data, addr = serv.recvfrom(4096)
        if not data: break
        data = data.decode()
        print("Data provided is: ")
        print(data)
        print('\n')

        if(data == "Done"):
            done = True
            break
        
        if(data == "RESET"):
            ipArr = np.empty(maxStudents,dtype=str)
        
        else:
            [pos,ipAddress] = parseIP(data)
            position = int(pos)
            updateIP(position,ipAddress)

            mess = "Done"
            message = mess.encode()
            sendMess(message,ipAddress)
            

#Thread 2
while True:
    for add in range (0,len(ipArr)):
        if(ipArr[add] != ''):
            ipAddress = ipArr[add]
            sendMess("runLED",ipAddress)
            waitTime = 0
            while(~done):
                if(waitTime >= maxTime):
                    ipArr[add] = ''
                    done = True
                waitTime = waitTime+1
            done = False