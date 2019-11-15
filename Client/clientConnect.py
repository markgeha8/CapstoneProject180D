# Code obtained and then modified from this source
# http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/


import socket
import fcntl
import struct

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

#Read in position(pos)
#Use code from Charlotte

#This is a filler for now
pos = 5
pos_string = str(pos)
init_msg = pos_string + "," + ip
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
        if(data == pos_string):
            init_bool = True
            print("server matches client")
        else:
            print("server doesn't match client")
            break

LED_displays = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]

#check that we have initialized the system

test_count = 0

while(init_bool):
    from_server = client.recvfrom(4096)
    data = (from_server[0]).decode()  #Temporary fix for Tuple issue
    #this data variable would actually be converted to an int
    testLED = data
    print(testLED)
    if(testLED == "testLED"):
        tested = "testDone"
        client.sendto(,(tested.encode(),'172.20.10.5',8080))
    from_server = client.recvfrom(4096)
    data = (from_server[0]).decode()  #Temporary fix for Tuple issue
    ##this data variable would actually be converted to an int
    runLED = data
    print(runLED)
    if(testLED == "runLED"):
        ran = "runDone"
        client.sendto(,(ran.encode(),'172.20.10.5',8080))
        print("running LED test_count")
    test_count += 1










#This will serve as a filler to see what we
client.close()
