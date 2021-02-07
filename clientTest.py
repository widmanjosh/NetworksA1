
import socket
from proxy import UDPServer
"""
client_sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

msg='hello UDP server'
client_sock.sendto(msg.encode("utf-8"),("127.0.0.1",12345))
data,addr=client_sock.recvfrom(4096)
print('Server says')
print(str(data.decode()))
client_sock.close()
"""

udp = UDPServer("127.0.0.1",82,1024)

