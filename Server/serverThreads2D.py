#https://wiki.python.org/moin/UdpCommunication
#https://www.geeksforgeeks.org/socket-programming-python/

import numpy as np
from scipy.ndimage import measurements
import socket
import time
from socket import AF_INET, SOCK_DGRAM
import fcntl
import struct
import threading
serv = socket.socket(AF_INET, SOCK_DGRAM)

serv.settimeout(10) #10 second delay per connection request

maxStudents = 84
maxRows = 20
maxCols = 20
deltaTime = 0.5
ipArr = np.empty([maxRows,maxCols],dtype=object)
done = False

ipArrBin = np.zeros([maxRows,maxCols],dtype=int)

#Gets IP address of server so others can connect (server's should be known by everyone beforehand)
def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s'.encode(), ifname[:15].encode())
        )[20:24])

#Parse the position and IP address String. Returns a list.
def parseIP(data):    
    parsed = data.split(',')
    return parsed

#Updates the IP array with the correct position
def updateIP(posR,posC,ipAddress):
    ipArr[posR-1,posC-1] = ipAddress #Index
    return

#Sends message to the Client in byte form
def sendMess(message,ipAddress):
    serv.sendto(message,(ipAddress,8080))
    return

#Create array of simple binary 0s and 1s to determine locations of where the IP addresses are
def createBinaryArray(ipArr):
    for r in range (0,maxRows):
        for c in range (0,maxCols):
            if(ipArr[r,c] == None):
                ipArrBin[r,c] == 0
            else:
                ipArrBin[r,c] == 1
    return ipArrBin

#Use built in functions in "measurements" library to determine clusters. These clusters will be cycled through
def clusterData():
    ipArrBin = createBinaryArray(ipArr)
    clustered, numberOfClusters = measurements.label(ipArrBin)
    return [clustered,numberOfClusters]

#Thread 1: Focuses on connecting Clients and adding their IP addresses to the overall IP array
def establishClientConnections():
    global done
    global ipArr

    while True:
        try:
            data, _ = serv.recvfrom(4096) #Sets up try/except block to ensure wait time isn't too long (cycles every 10 seconds)
        except socket.timeout:
            print("Timeout from establishing connection with a Client")
            continue
        if not data: continue
        data = data.decode()

        if(data == "iterDone"): #See if it is confirmation by the Client
            done = True
            data = ''
            continue
        
        else:
            if(data == "RESET"): #See if the whole IP array must be RESET because of a mistake
                ipArr = np.empty([maxRows,maxCols],dtype=object)
            
            else: #If all is good, parse the information, update the array, and confirm with that IP address
                [posR,posC,ipAddress] = parseIP(data)
                posRow = int(posR)
                posCol = int(posC)
                updateIP(posRow,posCol,ipAddress)

                mess = posR + ',' + posC
                message = mess.encode()
                sendMess(message,ipAddress)

        data = ''
        
#Thread 2: Focuses on sending messages to the Clients while everything is still happening
def propagateDisplayMessages():
    global done
    global ipArr
    iter = 0

    while True:
        [clusteredData,numberOfClusters] = clusterData()
        area = measurements.sum(ipArrBin, clusteredData, index=np.arange(clusteredData.max() + 1))
        for clustNum in range (1,numberOfClusters+1): #Move throughout clusters of students
            amountInClust = area[clustNum]
            numWithinClust = 0
            for posR in range (0,maxRows): #Move throughout the IP address loop
                for posC in range (0,maxCols):
                    if(not(ipArr[posR,posC] == None)): #"None" will define all the locations that are not connected
                        if(clusteredData[posR,posC] == clustNum):
                            numWithinClust = numWithinClust + 1
                            ipAddress = ipArr[posR,posC]
                            mess = str(clustNum) + ',' + str(amountInClust) + ',' + str(numWithinClust) #Sends them the code to start their LED run
                            message = mess.encode()
                            try: 
                                sendMess(message,ipAddress) #If they are not connected, this will be problematic and will cause the IP to be removed
                            except socket.timeout:
                                ipArr[posR,posC] = None
                                print("Timeout from IP address " + ipAddress)
                                continue
                                
                            startTime = time.time()
                            while(not done):
                                if(time.time()-startTime > deltaTime): #If there is no response for longer than maxTime iterations, it will be removed (failsafe)
                                    ipArr[posR,posC] = None
                                    print("Time Timeout from IP address " + ipAddress)
                                    break
                            
                            if(iter == 5):
                                print(ipArr[posR,posC])
                                print(numWithinClust)
                                print("____________")
                                iter = 0
                            iter = iter + 1
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
