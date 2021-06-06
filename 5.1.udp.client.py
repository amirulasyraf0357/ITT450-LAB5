import socket
import sys

ip = '192.168.56.101'
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

# Let's send data through UDP protocol
while True:

   s.sendto(b'Hi, saya client. Terima Kasih!', (ip, port)) #client send
   data, address = s.recvfrom(1024)
   print(data) #client receive

 # close the socket
s.close()