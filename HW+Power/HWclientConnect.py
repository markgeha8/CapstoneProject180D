import socket
import fcntl
import struct
import time
import random
import RPi.GPIO as GPIO

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



ip = get_ip_address('wlan0')
#Test print of IP address
print(ip)

#SEND INITIAL PROMPT TO TOKEN AND READ BACK IN THE ROW/COLUMN (CURRENTLY AN UNKNOWN IP ADDRESS BUT WILL KNOW ONCE WE GET HARDWARE)
#SHOULD BE SEPARATE DEFINED FUNCTION THAT CAN RUN INITIALLY THROUGH MAIN FUNCTION AND THEN HAVE A RECURSIVE THREAD THAT CONSTANTLY
#WAITS FOR PROMPTING FROM THE SERVER

#Button interupt - to get token( row col - data)

#This is a filler for now
#From Comms - string with row, column
test_coms = "5,5"
[posRow,posCol] = parseData(test_coms)
init_msg = test_coms + "," + ip
init_bool = False


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#enter server IP address - must be known beforehand
client.bind((ip, 8080))

while(not init_bool):
    client.sendto(init_msg.encode(),('172.20.10.5',8080))
    while(not init_bool):
        from_server = client.recvfrom(4096)
        data = (from_server[0]).decode()  #Temporary fix for Tuple issue
        if(data == "RESET"):
            print(data)
        [Row, Col] = parseData(data)
        if(Row == posRow & Col == posCol):
            init_bool = True
            print("server matches client")
        else:
            print("server doesn't match client")
            break

LED_displays = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]

#Testing script for LED_displays
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#pin numbers can change as needed
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

ran = "iterDone"
test_count = 5

while(init_bool & test_count<5 ):
    from_server = client.recvfrom(4096)
    data = (from_server[0]).decode()  #Temporary fix for Tuple issue

    #have token check -  send new token info to server

    #receive  ClusterNum, and AmountInClus, numWithinClust
    [ClustNum, AmIC, NumWC] = parseData(data)

    if(test_count<5):
        print("running LED: " + str(LED_displays[NumWC])+ " out of " + str(AmIC) + " LEDs.")
        if(NumWC== 1):
            GPIO.output(17,GPIO.HIGH)
            time.sleep(2)
            GPIO.output(17,GPIO.LOW)
            print("mode 1: turn on left LED.")
            
        if(NumWC == 2):
            GPIO.output(18,GPIO.HIGH)
            time.sleep(2)
            GPIO.output(18,GPIO.LOW)
            print("mode 2: turn on right LED.")
        if(NumWC == 3):
            GPIO.output(22,GPIO.HIGH)
            time.sleep(2)
            GPIO.output(22,GPIO.LOW)
            print("mode 3: turn on up LED.")
            
        if(NumWC == 4):
            GPIO.output(17,GPIO.HIGH)
            GPIO.output(18,GPIO.HIGH)
            GPIO.output(22,GPIO.HIGH)
            GPIO.output(23,GPIO.HIGH)
            time.sleep(2)
            GPIO.output(17,GPIO.LOW)
            GPIO.output(18,GPIO.LOW)
            GPIO.output(22,GPIO.LOW)
            GPIO.output(23,GPIO.LOW)
            print("mode 4: turn on down LED.")
    test_count += 1
    client.sendto(ran.encode(),('172.20.10.5',8080))











#This will serve as a filler to see what we
client.close()
