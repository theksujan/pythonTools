import scapy.all as scapy

def scan(ip):
    #   1. create request ->  2. send request -> 3. capture response
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    
    #  4. capture response into a list
    clients_list=[]
    for element in answered_list:
        clients_dict={"ip":element[1].psrc,"mac":element[1].hwsrc}
        clients_list.append(clients_dict)
    return clients_list

# 5. printing the scan results
def Print_result(result_list):
    print("IP\t\t\tMAC\n--------------------------------------------")
    for i in result_list:
        print(i["ip"]+"\t\t"+i["mac"])

scan_result=scan("10.0.2.0/24")
Print_result(scan_result)


