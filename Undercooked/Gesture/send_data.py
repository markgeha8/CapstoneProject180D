import time
import IMU
import socket
from socket import AF_INET, SOCK_DGRAM
import threading



send_data = "chop"
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



while True:
    client.sendto(send_data.encode(), ('192.168.1.182',8080))
