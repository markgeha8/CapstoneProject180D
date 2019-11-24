import socket
from socket import AF_INET, SOCK_DGRAM
import fcntl
import struct
import threading
import RPi.GPIO as GPIO

token = socket.socket(AF_INET, SOCK_DGRAM)

token.settimeout(10) #10 second delay per connection request

def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s'.encode(), ifname[:15].encode())
        )[20:24])

def changingDisplay():
    global row
    global col

    while True:
        #Insert code on taking input from buttons to increase/decrease value and cycle between r and c
        row = 1
        col = 2

def receiveClientIP():
    global row
    global col

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

        coordinates = str(row) + str(col)
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
