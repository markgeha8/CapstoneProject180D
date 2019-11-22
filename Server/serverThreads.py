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
ipArr = np.empty(maxStudents,dtype=object)
done = False

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
def updateIP(pos,ipAddress):
    ipArr[pos-1] = ipAddress
    return

#Sends message to the Client in byte form
def sendMess(message,ipAddress):
    serv.sendto(message,(ipAddress,8080))
    return

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
        print("Data provided is: ")
        print(data)
        print('\n')

        if(data == "runDone"): #See if it is confirmation by the Client
            done = True
            continue
        
        else:
            if(data == "RESET"): #See if the whole IP array must be RESET because of a mistake
                ipArr = np.empty(maxStudents,dtype=object)
            
            else: #If all is good, parse the information, update the array, and confirm with that IP address
                [pos,ipAddress] = parseIP(data)
                position = int(pos)
                updateIP(position,ipAddress)

                mess = pos
                message = mess.encode()
                sendMess(message,ipAddress)
            

#Thread 2: Focuses on sending messages to the Clients while everything is still happening
def propagateDisplayMessages():
    global done
    global ipArr

    while True:
        for add in range (0,len(ipArr)): #Move throughout the IP address loop
            if(ipArr[add] != None): #"None" will define all the locations that are not connected
                ipAddress = ipArr[add]
                try: 
                    mess = "runLED" #Sends them the code to start their LED run
                    message = mess.encode()
                    sendMess(message,ipAddress) #If they are not connected, this will be problematic and will cause the IP to be removed
                except socket.timeout:
                    ipArr[add] = None
                    print("Timeout from IP address " + ipAddress)
                    continue
                    
                waitTime = 0

                while(not done):
                    if(waitTime >= maxTime): #If there is no response for longer than maxTime iterations, it will be removed (failsafe)
                        ipArr[add] = None
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
