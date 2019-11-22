#https://wiki.python.org/moin/UdpCommunication
#https://www.geeksforgeeks.org/socket-programming-python/

import numpy as np
import socket
import socket.timeout as TimeoutException
import fcntl
import struct
serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serv.settimeout(30)
reset = True
kmax = 0

#Gets IP address of server so others can connect (should be known by everyone beforehand)
def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s'.encode(), ifname[:15].encode())
        )[20:24])

ip = get_ip_address('wlan0')
print(ip)
serv.bind((ip, 8080))

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
    

#Currently an infinite loop just in case the test goes wrong
while(reset):
    k = 0

    while True:
        while True:
            #Receive String of "position,IP address" from Clients
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

            k = k + 1

            recData = (recData).encode()

            serv.sendto(recData,(ipAdd,8080))

            #kmax is the maximum number of students in the class so that we can disconnect when we've gotten them all
            if (k > kmax):
                break
            
        if (k > kmax):
            break

    print("Parsing demo completed")

    #Collect all the IP addresses in order so they're easy to reach
    ipArr = []
    for k in range (0,len(iparray[0])):
        ipTemp = ""
        for temp in range (0,len(iparray[0,k])):
            ipTemp = ipTemp + iparray[0,k][temp]
        ipArr.append(ipTemp)

    #______________________________________________________________________________________________________#
    #Code Test

    for add in range (0,len(ipArr)):
        if(ipArr[add] != ''):
            ipAdd = ipArr[add]
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

    #Check if something is wrong (received a secondary "RESET" message)
    #Currently waits 30 seconds after the test is complete to see if something is wrong
    #https://stackoverflow.com/questions/37650716/python-fixed-wait-time-for-receiving-socket-data
    try:
        data, addr = serv.recvfrom(4096)
    except TimeoutException:
        print("Timeout! Try again...")
    if (data != "RESET"):
        reset = False


#______________________________________________________________________________________________________#
#Infinite Increment

while True:
    for add in range (0,len(ipArr)):
        if(ipArr[add] != ''):
            ipAdd = ipArr[add]
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

#Multithreading Idea:
#Global IP address array that will constantly update.
#One thread constantly listens for a Client connecting with a string that holds "position,IP address"
#and will constantly update Global IP address array.
#Other thread will use Global IP address array to run the tests and send messages to/receive messages from Clients.