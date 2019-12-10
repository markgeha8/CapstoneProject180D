import socket
import numpy as np
from socket import AF_INET, SOCK_DGRAM
import fcntl
import struct
import threading
import RPi.GPIO as GPIO
import time

# Constants
NUM_SEGS = 7
A = 11
B = 12
C = 13
D = 15
E = 16
F = 18
G = 22
S1 = 7
S2 = 29
S3 = 36
BN1 = 33
BN2 = 37
SW = 31
LED = 32

# Globals
token = socket.socket(AF_INET, SOCK_DGRAM)
position = np.zeros(2,dtype = int)
letter = 'r'
pos = 0

token.settimeout(10) #10 second delay per connection request

def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s'.encode(), ifname[:15].encode())
        )[20:24])

def increasePos():
    if(position[pos] == 21):
        position[pos] = 0
    else:
        position[pos] = position[pos] + 1

def decreasePos():
    if(position[pos] == 0):
        position[pos] = 21
    else:
        position[pos] = position[pos] - 1

def changeLetter():
    global pos

    if(letter == 'r'):
        letter = 'c'
        pos = 1
    else:
        letter = 'r'
        pos = 0

def displayNumber(integer):
    print(integer)

def displayLetter(letter):
    if(letter == 'r'):
        print('r')
    else:
        print('c')

def blinkSegment(segment, character):
    global A, B, C, D, E, F, G, NUM_SEGS
    timeDelay = 0.0001

    mask = 0x01

    led = [A, B, C, D, E, F, G]

    GPIO.output(segment, 0)

    for i in range (0, NUM_SEGS):
        tmp = (character >> i) & mask
        if(tmp == 0x01):
            GPIO.output(led[i], 1)
            time.sleep(timeDelay)
            GPIO.output(led[i], 0)
        else:
            time.sleep(timeDelay)
            GPIO.output(led[i], 0)

    GPIO.output(segment, 1)


def characterToDisplay(character):
    if (character == 'r'):
        return 0x50
    elif (character == 'c'):
        return 0x58
    else:
        return 0x00

def integerToDisplay(integer):
    switcher = {
        0: 0x3F,
        1: 0x06,
        2: 0x5B,
        3: 0x4F,
        4: 0x66,
        5: 0x6D,
        6: 0x7D,
        7: 0x07,
        8: 0x7F,
        9: 0x6F,
    }
    return switcher.get(integer, 0x00)

def changingDisplay():
    global pos
    global letter
    GPIO.setmode(GPIO.BOARD)
    chan_list_in = [31,33,37]
    chan_list_out = [7,11,12,13,15,16,18,22,29,32,36]
    GPIO.setup(chan_list_in,GPIO.IN)
    GPIO.setup(12,GPIO.OUT)
    GPIO.add_event_detect(31, GPIO.BOTH, callback=changeLetter, bouncetime = 300)
    GPIO.add_event_detect(33, GPIO.FALLING, callback=increasePos, bouncetime=300)
    GPIO.add_event_detect(37, GPIO.FALLING, callback=decreasePos, bouncetime=300)

    while True:
        blinkSegment(S1, characterToDisplay(letter))
        blinkSegment(S2, integerToDisplay(position[pos]%10))
        blinkSegment(S2, integerToDisplay(position[pos]/10))

        
def receiveClientIP():
    global pos
    global letter

    while True:
        try:
            ipAddress, _ = token.recvfrom(4096) #Sets up try/except block to ensure wait time isn't too long (cycles every 10 seconds)
        except socket.timeout:
            print("Timeout from establishing connection with a Client")
            continue
        if not ipAddress: continue
        ipAddress = ipAddress.decode()
        print("ipAddress provided is: ")
        print(ipAddress)
        print('\n')

        row = position[pos]
        col = position[pos]
        coordinates = str(row) + ',' + str(col)
        coordinates = coordinates.encode()
        token.sendto(coordinates,(ipAddress,8080))

# Main function
if __name__ == "__main__":
    ip = get_ip_address('wlan0') #'172.20.10.5'
    print(ip)
    token.bind((ip, 8080))

    # creating thread 
    t1 = threading.Thread(target=changingDisplay, args=()) 
    t2 = threading.Thread(target=receiveClientIP, args=()) 
  
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
