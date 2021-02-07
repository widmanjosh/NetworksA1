#takes in a port number as an arg can not be hard coded
#sample call
#python proxy.py 8888

import socket
from urllib.parse import urlparse
from client import Client
import sys
import os.path
from os import path
import csv
from csv import writer

import codecs


class UDPServer:
    def __init__(self,server,port,buffSize):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.buffSize = buffSize
        self.cache = {}
        self.cacheLocation = "cache.csv"


        if str.isnumeric(server[0]):
            self.server = server
            self.ip = server
        else:
            self.server = server
            self.ip = socket.gethostbyname(server)

        #bind to socket

        self.sock.bind((self.ip, self.port))


        self.sock.listen(20)
        self.initCache()
        print("done init")

    def initCache(self):

        if(path.exists('cache.txt')):
            f = open("cache.csv","w")
            #f.write("key,data\n")
            f.close()
            self.loadFromCSV()
        else:
            f = open("cache.csv","w+")
            f.write("key,data\n")
            f.close()
        return

    def loadFromCSV(self):
        reader = csv.DictReader(open(self.cacheLocation, 'rb'))
        dict_list = []
        for line in reader:
            dict_list.append(line)
        self.cache =  dict_list

        return


    def insertToCache(self,key,data):
        print("called")
        self.cache[key] = data
        with open(self.cacheLocation,"a+",newline='') as f:
            csv_writer = writer(f)
            csv_writer.writerow([key,data])
            print("{} {}".format(key,data))

        return





    def query(self,path):

        query = urlparse(path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        imsi = query_components["imsi"]
        return imsi




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

    def startListening(self):

        print('about to accept connection')
        con, addr = self.sock.accept()
        print('connection accepted')

        i = 0
        with con:
            while True:
                print('number of loops: {}'.format(i))
                data, addr = con.recvfrom(self.buffSize)

                httpRequest = data.decode('utf-8').strip().split("\n")[0]

                if not data:
                    break
                else:
                    if not ('favicon' in httpRequest):

                        if httpRequest in self.cache:
                            processData = self.cache[httpRequest]
                        else:
                            processData = self.processRequest(httpRequest)
                            self.insertToCache(httpRequest,processData)

                        print('Sending processed Data')
                        #con.sendto(bytes(processData.encode()), (self.server, self.port))
                        con.send(bytes(processData.encode()))

                i +=1



        print('Closed connection')
        self.sock.close()


    def processRequest(self,request):


        serverName = self.serachForHost(request)
        r = self.formatRequest(serverName)

        print('Client server name:{}'.format(request))
        c = Client(serverName,80,self.buffSize)
        c.connect()

        print("Sending Message:{}".format(r))
        c.sendMessage(r)
        print('message sent')
        print('receving data')
        data, addr = c.recvAllFrom()
        print('Done receiving')
        c.socket.send(bytes('HTTP/1.0 200 OK\n'.encode()))
        print('Sent okay request')


        c.socket.close()


        print('Done')

        return data



print('Started Program')
udp = UDPServer("127.0.0.1",83,1024)
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