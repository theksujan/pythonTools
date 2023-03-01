import socket

target_host = 'www.google.com'
target_port = 80

#create socket object
client = socket.socket()

#connect to target 
client.connect((target_host,target_port))

#send some data
client.send(b'HEAD / HTTP/1.1\r\nHOST:google.com\r\n\r\n')

#receive some data
response = client.recv(4096)
print(response.decode())

