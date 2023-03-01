import argparse
import subprocess
import sys
import shlex
import textwrap
import socket


def execute(cmd):
    cmd = cmd.strip() #removing leading and trailing white spaces
    
    output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT) 
    print(output.decode())
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BHP Net Tool',formatter_class=argparse.RawDescriptionHelpFormatter,epilog=textwrap.dedent('''Example: netcat.py -t 192.168.193.70 -p 4444 -l  -c #command shell
netcat.py -t 192.168.193.70 -p 4444 -l -u=mytest.txt #upload to file  netcat.py -t 192.168.193.70 -p 4444 -e = \"cat /etc/passwd\" #execute a command
echo 'ABC'| ./netcat.py -t 192.168.193.70 -p 135 #echo to server at port 135
netcat.py -t 192.168.193.70 -p 4444 #connect to server'''))
    
parser.add_argument('-c','--command',action='store_true',help='command shell')
parser.add_argument('-e','--execute',action='store_true',help='execute specified command')
parser.add_argument('-l','--listen',action='store_true',help='listen')
parser.add_argument('-p','--port', type=int,help='specified port',default=4444)
parser.add_argument('-t','--target',action='store_true',help='specified target ip')
parser.add_argument('-u','--upload',action='store_true',help='upload file')
args = parser.parse_args

if args.listen:
    buffer = ''
else:
    buffer = sys.stdin.read()



class NetCat:
    def __init__(self,args,buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
            
#writing send method of netcat class

def send(self):
    #connect
    self.socket.connect((self.args.target,self.args.port))
    #send
    if self.buffer:
        self.socket.sendall(self.buffer)
    
    #continue to receive data 
    while True:
        data = self.socket.recv(4096)
        if not data:
                break
        print(data.decode())
        
nc = NetCat(args,buffer.encode())
nc.run()
            
buffer = input('>')
nc.socket.sendall(buffer.encode())