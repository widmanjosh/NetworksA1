#sends an http request to a server and prints the response from the server.
import socket
client_sock=

class Client:

    def __init__(self,server,port,bufferSize):
        self.port = port
        self.server = server
        self.bufferSize = bufferSize
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    #takes a message for client to send and sends to current server
    def sendMessage(self,msg):
        self.socket.sendto(msg.encode("utf-8"),(self.server,self.port))
        return

    #receive all funciton - not sure how to tell if all information is in buffer from instructions
    #**** come back too ***
    def recvAllFrom(self):
        data,addr = self.socket.recvfrom(self.bufferSize)
        return data,addr

    msg='hello UDP server'
client_sock.sendto(msg.encode("utf-8"),("127.0.0.1",12345))
data,addr=client_sock.recvfrom(4096)
print('Server says')
print(str(data.decode()))
client_sock.close()