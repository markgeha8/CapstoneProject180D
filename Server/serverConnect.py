# Reminder: This is a comment. The first line imports a default library "socket" into Python.
# You don’t install this. The second line is initialization to add TCP/IP protocol to the endpoint.
import numpy as np
import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

iparray = np.empty((1,40,16),dtype=str)

#Test/Demo Purposes
data = ["14,10.15.32.15", "RESET", "1,234.520.134.253"]
k = 0

# Assigns a port for the server that listens to clients connecting to this port.
serv.bind(('0.0.0.0', 8080))
#serv.listen(40) #Assuming there will be 40 RPis attempting to connect (or something like that)
while True:
    #conn, addr = serv.accept()
    while True:
        #data = conn.recv(4096)
        #if not data: break
        #data.decode()
        print("Data provided is: ")
        print(data[k])
        print('\n')

        recData = ""

        #Empty the array if the received data is a RESET function
        if(data[k] == "RESET"):
            del iparray[:]
            iparray = np.empty((1,40,16),dtype=str)
            recData = "Reset"

        #Parse the data into position and IP address.
        else:
            posBool = True
            ipBool = True
            pos = ""
            ip = ""
            i = 0
            while posBool:
                if(data[k][i] == ','):
                    posBool = False
                    i = i+1
                    break
                pos = pos + data[k][i]
                i = i+1
            
            while ipBool:
                if(i >= len(data[k])):
                    ipBool = False
                    break
                ip = ip + data[k][i]
                i = i+1

            #Add the IP address to the array of IP addresses that will later be referenced
            for j in range (0, len(ip)-1):
                iparray[(0,int(pos)-1)][j] = ip[j]

            recData = pos

        print("iparray[")
        print(int(pos)-1)
        print("]: ")
        for l in range (0,len(iparray[int(pos)-1])-1):
            print(iparray[int(pos)-1][l])
        print('\n')

        if(k == 2):
            k = 0
            break

        k = k+1
        break

        #conn.send((recData).encode())
    #conn.close()
    #print('Client Disconnected')
    