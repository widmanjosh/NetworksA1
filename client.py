#sends an http request to a server and prints the response from the server.
import socket


class Client:

    #create client object to store connection details
    def __init__(self,server,port,bufferSize):


        self.port = port
        self.bufferSize = bufferSize

        if str.isnumeric(server[0]):
            self.server = server
            self.ip = server
        else:
            self.server = server
            self.ip = socket.gethostbyname(server)

        #SOCK_DGRAM
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        #self.socket.bind((self.server,self.port))

    #takes a message for client to send and sends to current server
    def sendMessage(self,msg):
        self.socket.sendto(bytes(msg.encode()),(self.server,self.port))
        return

    #receive all funciton - not sure how to tell if all information is in buffer from instructions
    #**** come back too ***
    def recvAllFrom(self):

        #Used to append all data received from site
        totalSiteData = ""
        lastAddr = ""
        data = "-1"
        #keep pulling until there is no data returned
        while len(data) >0:

            data,addr = self.socket.recvfrom(self.bufferSize)
            totalSiteData = totalSiteData + data.decode()
            print(data.decode())
            lastAddr = addr


        return totalSiteData,lastAddr

    def connect(self):

        self.socket.connect((self.ip,self.port))

        return

def main():
    hostName = "www.apache.org"
    print('main ran')
    c = Client(hostName,80,1024)
    c.connect()

    c.sendMessage("GET / HTTP/1.1\r\nHost: webcode.me\r\nAccept: text/html\r\nConnection: close\r\n\r\n")
    data,addr = c.recvAllFrom()
    print(data)

    """
    #sock.bind(('127.0.0.1', 12345))
    c.sendMessage(GET / HTTP/1.1\r\nHost:{}\r\n\r\n.format(c.server))
    response = c.socket.recv(c.bufferSize)
    print(len(response))
    #data,addr = c.recvAllFrom()
    #print(data)
    """
    print(c.server)
    print(c.ip)

if __name__ == "__main__":
    main()
