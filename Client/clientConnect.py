import socket
from socket import AF_INET, SOCK_DGRAM
import fcntl
import struct
import time
import random
import RPi.GPIO as GPIO
import threading
import cv2

init_bool = False
test_count = 1
test_num = 0
posRow = 0
posCol = 0
connect = True
connected = False

ipToken = '172.20.10.11'
ipServer = '172.20.10.5'

#Parse the position and IP address String. Returns a list.
def parseData(data):
    parsed = data.split(',')
    return parsed

#Read in IP
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s'.encode(), ifname[:15].encode())
    )[20:24])

def connectToToken():
    global posRow, posCol
    global ip
    global connect
    global ipToken

    client.sendto(ip.encode(),(ipToken,8080))
    try:
        from_token, _ = client.recvfrom(4096) #Sets up try/except block to ensure wait time isn't too long (cycles every 10 seconds)
        data = (from_token).decode()
        [posRow,posCol] = parseData(data)
        connect = False
    except socket.timeout:
        print("Timeout from establishing connection with a Token")



def establishServerConnections():
    global init_bool
    global posRow, posCol
    global connect
    global connected
    global ipServer

    #GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(13,GPIO.IN)
    #GPIO.setwarnings(False)
    #GPIO.add_event_detect(13, GPIO.RISING, callback=connectToToken, bouncetime=300)

    while True:
        #Test print of IP address
        ip = get_ip_address('wlan0')
        
        while(connect):
            input("Press Enter to connect...")
            connectToToken()

        test_coms = posRow + ',' + posCol
        init_msg = test_coms + "," + ip

        while(not init_bool):
            print("Row: ", posRow, " Col: ", posCol)
            print("Connecting...")
            client.sendto(init_msg.encode(),(ipServer,8080))
            while(not init_bool):
                try:
                    from_server = client.recvfrom(4096) #Sets up try/except block to ensure wait time isn't too long (cycles every 10 seconds)
                except socket.timeout:
                    print("Timeout from establishing connection with a Server")
                    continue
                data = (from_server[0]).decode()  #Temporary fix for Tuple issue
                if(data == "RESET"):
                    print(data)
                [Row, Col] = parseData(data)
                if((Row == posRow) and (Col == posCol)):
                    init_bool = True
                    print("server matches client")
                    connected = True
                else:
                    print("server doesn't match client")
                    break

LED_displays = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]


def DisplayLoop():
    global test_count
    global test_num
    global connected

    while True:
        while connected:
            #Testing script for LED_displays
            #GPIO.setmode(GPIO.BCM)
            #GPIO.setwarnings(False)

            #pin numbers can change as needed
            #GPIO.setup(17, GPIO.OUT)
            #GPIO.setup(18, GPIO.OUT)
            #GPIO.setup(22, GPIO.OUT)
            #GPIO.setup(23, GPIO.OUT)

            ran = "iterDone"
            try:
                from_server, _ = client.recvfrom(4096) #Sets up try/except block to ensure wait time isn't too long (cycles every 10 seconds)
            except socket.timeout:
                print("Timeout from establishing connection with a Server")
                continue
            data = (from_server).decode()  #Temporary fix for Tuple issue
            #have token check -  send new token info to server

            #receive  ClusterNum, and AmountInClus, numWithinClust
            [ClustNum, AmIC, NumWC] = parseData(data)
            print(NumWC)

            while((init_bool) and (test_count < 2)):


                if(test_count<2):
                    print("running LED: " + "Cluster Number: " + str(ClustNum) + ', ' + str(LED_displays[int(NumWC)])+ " out of " + str(AmIC) + " LEDs.")
                    if(int(NumWC)== 1):
                        #GPIO.output(17,GPIO.HIGH)
                        #time.sleep(2)
                        #GPIO.output(17,GPIO.LOW)
                        print("pattern 1")

                    if(int(NumWC) == 2):
                        #GPIO.output(18,GPIO.HIGH)
                        #time.sleep(2)
                        #GPIO.output(18,GPIO.LOW)
                        print("pattern 2")

                    if(int(NumWC) == 3):
                        #GPIO.output(22,GPIO.HIGH)
                        #time.sleep(2)
                        #GPIO.output(22,GPIO.LOW)
                        print("pattern 3")
                    if(int(NumWC) == 4):
                        print("pattern 4")
                        print("hi")
                    test_num += 1
                test_count += 1
                client.sendto(ran.encode(),(ipServer,8080))

            test_count = 0





# Main function
if __name__ == "__main__":
    global ip
    ip = get_ip_address('wlan0') #'172.20.10.5'
    print(ip)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(10)

    #enter server IP address - must be known beforehand
    client.bind((ip, 8080))

    # creating thread
    t1 = threading.Thread(target=establishServerConnections, args=())
    t2 = threading.Thread(target=DisplayLoop, args=())

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
