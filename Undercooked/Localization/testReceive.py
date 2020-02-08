import socket
from socket import AF_INET, SOCK_DGRAM

serv = socket.socket(AF_INET, SOCK_DGRAM)
serv.bind(('172.20.10.6', 8080))
serv.settimeout(10)

while True:
    try:
        data, _ = serv.recvfrom(4096)
    except socket.timeout:
        print("Timeout without connecting to Client")
        continue
    if not data:
        continue
    print(data.decode())

