#takes in a port number as an arg can not be hard coded
#sample call
#python proxy.py 8888

import socket
from urllib.parse import urlparse
from client import Client

import codecs


class UDPServer:
    def __init__(self,server,port,buffSize):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.buffSize = buffSize


        if str.isnumeric(server[0]):
            self.server = server
            self.ip = server
        else:
            self.server = server
            self.ip = socket.gethostbyname(server)

        #bind to socket

        self.sock.bind((self.ip, self.port))


        self.sock.listen(20)




    def query(self,path):

        query = urlparse(path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        imsi = query_components["imsi"]
        return imsi

    def startListening(self):

            print('about to accept connection')
            con, addr = self.sock.accept()
            print('connection accepted')

            try:
                with con:
                    while True:

                        data, addr = con.recvfrom(self.buffSize)


                        if not data:
                            break



                        processData = self.processRequest(data.decode('utf-8').strip().split("\n")[0])

                        print('Sending processed Data')
                        con.sendall(processData)

            except Exception as e:
                print(e)
                print('Error happened and connection was closed')
                self.sock.close()
            print('Closed connection')
            self.sock.close()



    def sendMessage(self,msg):
        self.socket.sendto(bytes(msg.encode()),(self.server,self.port))
        return

    def recvAllFrom(self):

        #Used to append all data received from site
        totalSiteData = ""
        lastAddr = ""
        data = "-1"
        #keep pulling until there is no data returned
        while len(data) >0:
            print(len(data))
            data,addr = self.socket.recvfrom(self.bufferSize)
            totalSiteData = totalSiteData + data.decode()
            print(data.decode())
            lastAddr = addr

        return totalSiteData,lastAddr

    def serachForHost(self,request):
        #print('starting request :{}'.format(request))
        return request[request.find("/")+1:request.rfind(" ")]

    def formatRequest(self,server):
        return "GET / HTTP/1.1\r\nHost:{}\r\n\r\n".format(server)

    def processRequest(self,request):

        print("host test: {}".format(self.serachForHost(request)))
        serverName = self.serachForHost(request)
        r = self.formatRequest(serverName)

        c = Client(serverName,80,self.buffSize)
        c.connect()

        print("Sending Message:{}".format(r))
        c.sendMessage(r)
        print('message send')
        data, addr = c.recvAllFrom()

        print('Done')

        return data




print('Started Program')
udp = UDPServer("127.0.0.1",82,1024)
print('Start Server')
udp.startListening()


    #send back to client
    #print(str(data.decode()) + "testing")
    #message=bytes('Hello I am UDP Server'.encode("utf-8"))
    #self.sock.sendto(message,addr)



"""

import socket
import time
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    host = "127.0.0.1"
    port = 80

    s.connect((host, port))
    s.sendall(b'hello there')
    print(str(s.recv(4096), 'utf-8'))


with socket.socket() as s:

    host = 'localhost'
    port = 80

    s.bind((host, port))
    print(f'socket binded to {port}')

    s.listen()

    con, addr = s.accept()

    with con:

        while True:

            data = con.recv(1024)

            if not data:
                break

            con.sendall(data)



"""