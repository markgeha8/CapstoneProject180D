import time
import socket
from socket import AF_INET, SOCK_DGRAM
import threading



send_data = "chop"
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



while True:
    client.sendto(send_data.encode(), ('172.20.10.6',8080))
