from socket import *
import sys
from proxy import UDPServer


if len(sys.argv) <= 1:
    print('Usage : python proxy.py server_port\n')
    sys.exit(2)

    #your code goes here

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)


#your code goes here

while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = ''#your code goes here
    
    print(message)

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)

    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        print("Checkking to see if file exists")
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")
       
        #your code goes here

        print('Read from cache')
        
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":

            # Create a socket on the proxyserver
            c = '' #your code goes here 

            hostn = hostname.replace("www.","",1)

            try:
                # Connect to port 80 on server

                #your code goes here

                # Create a temporary file on this socket and ask port 80
                #for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                fileobj.write("GET "+"http://" + filename + "HTTP/1.0\n\n")

                # Read the response into buffer
                #your code goes here
                
                # Create a new file in the cache for the requested file.

                # Also send the response in the buffer to client socket
                #and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")

            except error as e :  
                print(e)
                print("Illegal request")
        else:
            # HTTP response message for file not found
            # Fill in start.
            # Fill in end.
    
            # Close the client and the server sockets
            c.close()
            
tcpCliSock.close()
