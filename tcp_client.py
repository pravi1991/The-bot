import socket

host='localhost'
port=3999

#create a tcp socket object
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#connect the client
client.connect((host,port))

#send some data 
client.send(b"GET / HTTP/1.1\r\Host: localhost\r\n\r\n")

#receive some data  
response = client.recv(4096)
print(response.decode('utf-8'))
