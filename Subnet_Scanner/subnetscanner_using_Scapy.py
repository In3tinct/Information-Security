#A simple subnet host scanner using python and scapy library

from scapy.all import *
import netifaces
#from netaddr import IPNetwork
import netaddr
import re

#Calculating the CIDR of the netmask
def calculateCIDR(networkmask):
        binary_str = ''
        for octet in networkmask:
                binary_str += bin(int(octet))[2:].zfill(8)
        return str(len(binary_str.rstrip('0')))

#To find local ip address and net mask
eth_address=netifaces.ifaddresses("eth0")
ip_and_mask = eth_address[socket.AF_INET][0]

print "Your IP address: "+ip_and_mask['addr']
print "Your net mask: "+ip_and_mask['netmask']

#All of this is not of use anymore, but still kept to print network address
#It finds network address which can be used to search the network
#A general method is to XOR the mask and ip address to get network address
concat_value=str(ip_and_mask['addr']+"/"+ip_and_mask['netmask'])
network_address=str(netaddr.IPNetwork(concat_value).cidr)
#network_address was having CIDR appeneded to it so removing it
network_ip=re.sub(r'\s', '', network_address).split('/')
print "Your network address is:"+network_ip[0]


#New addition
#Formatting IP and CIDR to fetch the list of IP in the subnet
ip_and_cidr = ip_and_mask['addr']+'/'+calculateCIDR(ip_and_mask['netmask'].split('.'))

#Gives a list of all hosts in the network
network_range =  list(netaddr.IPNetwork(ip_and_cidr))

#Removing network and broadcast address
del network_range[0]
network_range.pop()

print "********************Scanning********************"

for ip in network_range:
	formatted_ip=str(ip)
		
	#Creating an arp request, ethernet packet mush have broadcast address as
	#destination address as it would broadcast to all host, ARP hwdst could 	#be anything, since only the ip 
	#matters here, arp reply will have the mac of the host in return	
	arpRequest=Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=formatted_ip,hwdst="00:00:00:00:00:00")
	arpResponse=srp1(arpRequest,timeout=2,verbose=0)
	if arpResponse:
		print "Host is  up, IP:"+arpResponse.psrc+" MAC: "+arpResponse.hwsrc

print "Scanning completed"
