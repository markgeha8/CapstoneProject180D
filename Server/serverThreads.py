#https://wiki.python.org/moin/UdpCommunication
#https://www.geeksforgeeks.org/socket-programming-python/

import numpy as np
import socket
from socket import AF_INET, SOCK_DGRAM
import fcntl
import struct
import threading
serv = socket.socket(AF_INET, SOCK_DGRAM)

serv.settimeout(10)

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
    pos = ""
    ip = ""
    for i in range (0,len(data)):
        if(data[i] == ','):
            posBool = False
            continue
        if(posBool):
            pos = pos + data[i]  
        else:
            ip = ip + data[i]

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
def establishClientConnections():
    global done
    global ipArr

    while True:
        try:
            data, _ = serv.recvfrom(4096)
        except socket.timeout:
            print("Timeout from establishing connection with a Client")
            continue
        if not data: continue
        data = data.decode()
        print("Data provided is: ")
        print(data)
        print('\n')

        if(data == "Done"):
            done = True
            continue
        
        if(data == "RESET"):
            ipArr = np.empty(maxStudents,dtype=str)
        
        else:
            [pos,ipAddress] = parseIP(data)
            position = int(pos)
            updateIP(position,ipAddress)

            mess = pos
            message = mess.encode()
            sendMess(message,ipAddress)
            

#Thread 2
def propagateDisplayMessages():
    while True:
        for add in range (0,len(ipArr)):
            if(ipArr[add-1] != ''):
                ipAddress = ipArr[add]
                try: 
                    mess = "runLED"
                    message = mess.encode()
                    sendMess(message,ipAddress)
                except socket.timeout:
                    ipArr[add] = ''
                    print("Timeout from IP address " + ipAddress)
                    continue
                    
                waitTime = 0

                while(~done):
                    if(waitTime >= maxTime):
                        ipArr[add] = ''
                        break
                    waitTime = waitTime+1
                done = False

# Main function
if __name__ == "__main__":
    ip = get_ip_address('wlan0') #'172.20.10.5'
    print(ip)
    serv.bind((ip, 8080))

    # creating thread 
    t1 = threading.Thread(target=establishClientConnections, args=()) 
    t2 = threading.Thread(target=propagateDisplayMessages, args=()) 
  
    # starting thread 1 
    t1.start() 
    # starting thread 2 
    t2.start()

    # wait until thread 1 is completely executed 
    t1.join() 
    # wait until thread 2 is completely executed 
    t2.join() 
  
    # both threads completely executed 
    print("Done!")
