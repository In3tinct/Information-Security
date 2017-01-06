#A simple subnet host scanner using python and scapy library

from scapy.all import *
import netifaces
from netaddr import IPNetwork
import re

#To find local ip address and net mask
eth_address=netifaces.ifaddresses("eth0")
ip_and_mask = eth_address[socket.AF_INET][0]

print "Your IP address: "+ip_and_mask['addr']
print "Your net mask: "+ip_and_mask['netmask']

#It finds network address which can be used to search the network
#A general method is to XOR the mask and ip address
concat_value=str(ip_and_mask['addr']+"/"+ip_and_mask['netmask'])
network_address=str(IPNetwork(concat_value).cidr)

#network_address was having CIDR appeneded to it so removing it
network_ip=re.sub(r'\s', '', network_address).split('/')

print "Your network address:"+network_ip[0]

network_ip=re.sub(r'\s', '', network_ip[0]).split('.')
network_ip_string=str(network_ip[0]+"."+network_ip[1]+"."+network_ip[2]+".")

print "********************Scanning********************"
#Testing for initial 50 hosts only
for i in range(0,50):
	ip=network_ip_string+str(i)
	
	#Creating an arp request, ethernet packet mush have broadcast address as
	#destination address as it would broadcast to all host, ARP hwdst could 	#be anything, since only the ip 
	#matters here, arp reply will have the mac of the host in return
	arpRequest=Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip,hwdst="00:00:00:00:00:00")
	arpResponse=srp1(arpRequest,timeout=2,verbose=0)
	if arpResponse:
		print "Host is  up, IP:"+arpResponse.psrc+" MAC: "+arpResponse.hwsrc
		print ""
