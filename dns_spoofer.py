from scapy.all import * 
from  scapy.layers.dns import DNS,IP,UDP,DNSRR,DNSQR
import netfilterqueue

def process_packet(packet):
    scapy_packet=IP(packet.get_payload())
    #if scapy_packet.haslayer(DNS):
    print(scapy_packet.show())
    packet.accept()
  
queue= netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()
