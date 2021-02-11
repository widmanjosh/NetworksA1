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
import multiprocessing

import codecs




class UDPServer():
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
        #print('Full Request: {}'.format(request))

        request = request[request.find("/")+1:]
        endIndex = min(request.find(" "),request.find("/"))

        request = request[:endIndex]


        return  request



    def formatRequest(self,server,request):
        #print('Request to format :{}'.format(request))
        #print('new request: {}'.format("HTTP/1.1\r\nHost:{}".format(request[request.find('/')+1:])))
        #print('request to format {}'.format(request))
        #fRequest = request[request.find('/')+1:]
        #fRequest = fRequest[:fRequest.find(" ")]
        #print("new formated request:{}".format("""GET / HTTP/1.1\r\nHost:{}\r\n\r\n""".format(fRequest)))
        #return "GET / HTTP/1.1\r\nHost:{}\r\n\r\n".format(server)
        return """GET / HTTP/1.1\r\nHost:{}\r\n\r\n""".format(server)





    def startListening(self):

        #print('about to accept connection')
        con, addr = self.sock.accept()
        #print('connection accepted')

        i = 0
        with con:
            while True:
                #process = multiprocessing.Process(target=handle, args=(conn, address))
                #process.daemon = True
                #process.start()
                #print("Started process {}".format(process))

                print('number of loops: {}'.format(i))
                if i < 1:
                    data, addr = con.recvfrom(self.buffSize)
                    httpRequest = data.decode('utf-8').strip().split("\n")[0]
                    print("Current HTTP Request: {}".format(httpRequest))
                if not data:
                    break
                else:
                    try:
                        if i < 1:
                            print('Http request: {}'.format(httpRequest))

                            if not ("https" in httpRequest.lower()):
                                if httpRequest in self.cache:
                                    print('Site was cached')
                                    processData = self.cache[httpRequest]
                                else:
                                    print('Not Cached must process')
                                    processData = self.processRequest(httpRequest,None)
                                    self.insertToCache(httpRequest,processData)
                                    con.send(bytes(processData.encode()))

                            else:


                                con.sendall(bytes('HTTP/1.0 200 OK\n'.encode()))
                                con.sendall(bytes('Content-Type: text/html\n'.encode()))
                                con.sendall(bytes('\n'.encode()))  # header and body should be separated by additional newline
                                if len(httpRequest) <1:
                                    print('Invalid request entered')
                                    con.sendall(bytes(self.getHTMLCode("invalidRequest")))
                                else:
                                    print('other error')
                                    con.sendall(bytes(self.getHTMLCode("https").encode()))

                                print("sent error message")
                        else:
                            print('Multiple Request {}:{}'.format(i,httpRequest))
                    except:
                        con.sendall(bytes('HTTP/1.0 200 OK\n'.encode()))
                        con.sendall(bytes('Content-Type: text/html\n'.encode()))
                        con.sendall(bytes('\n'.encode()))  # header and body should be separated by additional newline
                        con.sendall(bytes(self.getHTMLCode("error")))
                if i > 1:
                    break
                i +=1



        print('Closed connection')
        self.sock.close()

    def getHTMLCode(self,et):
        if  "https" in et:
            return """<!DOCTYPE html><html><head><title>Https Request Rejected</title></head><body><center><h1>Https requests are not supported. Please use a website with a http request instead.</h1></center></body></html>\  """
        elif et == "invalidRequest":
            return """<!doctype html><html><head><title>Https Request Rejected</title></head><body><center><h1>Https requests are not supported. Please use a website with a http request instead.</h1></center></body></html>"""
        elif "400 Bad Request " in et:
            return """<!doctype html><html><head><title>Error 400: Bad Request</title></head><body><center><h1>The website that you are trying to reach gives a bad request error. Please try again with another website.</h1></center></body></html>"""
        elif "404 Not Found" in et:
            return """<!doctype html><html><head><title>Error 404: Page Not Found</title></head><body><center><h1>The website that you are trying to reach gives a page not found error. Please try again with another website.</h1></center></body></html>"""
        elif "500 Internal Server Error" in et:
            return """<!doctype html><html><head><title>Error 500: Internal Server Error</title></head><body><center><h1>The website that you are trying to reach gives an internal server error.</h1></center></body></html>"""
        elif "error":
            return """<!doctype html><html><head><title>Server Error</title></head><body><center><h1>The server encountered an error when trying to process your request. Please try again.</h1></center></body></html>"""




    def processRequest(self,request,serverName):

        if None == serverName:
            print('Was null')
            serverName = self.serachForHost(request)
        else:
            print('Called {},{}'.format(request,serverName))

        r = self.formatRequest(serverName,request)
        #r = request
        print('Searching for host:{}'.format(serverName))
        print('Request: {}'.format(r))

        print('Client server name:{}'.format(serverName))
        try:
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
        except:
            data = ""

        print('Done')

        #handel move


        return data



print('Started Program')
udp = UDPServer("127.0.0.1",81,1024)
print('Start Server')
udp.startListening()
for process in multiprocessing.active_children():
    print("shutting down process {}".format(process))
    process.terminate()
    process.join()



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