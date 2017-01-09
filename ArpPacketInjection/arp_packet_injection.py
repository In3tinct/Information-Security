#A simple subnet host scanner using python and scapy library

import socket
import netifaces
#from netaddr import IPNetwork
import netaddr
import re
from uuid import getnode as get_mac
import struct
import binascii

#Calculating the CIDR of the netmask
def calculateCIDR(networkmask):
        binary_str = ''
        for octet in networkmask:
                binary_str += bin(int(octet))[2:].zfill(8)
        return str(len(binary_str.rstrip('0')))

#Binding the socket with the ethernet port and ip protocol
raw_socket=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))
raw_socket.bind(('eth0',socket.htons(0x0800)))

#To find local ip address and net mask
eth_address=netifaces.ifaddresses("eth0")
ip_and_mask = eth_address[socket.AF_INET][0]

print "Your IP address: "+ip_and_mask['addr']
print "Your net mask: "+ip_and_mask['netmask']

#Formatting IP and CIDR to fetch the list of IP in the subnet
ip_and_cidr = ip_and_mask['addr']+'/'+calculateCIDR(ip_and_mask['netmask'].split('.'))

#Gives a list of all hosts in the network
network_range =  list(netaddr.IPNetwork(ip_and_cidr))

print "Your network address is:%s"%str(network_range[0])

#Removing network and broadcast address
del network_range[0]
network_range.pop()

#Getting the MAC address
ip_source=socket.inet_aton(str(ip_and_mask['addr']))
#mac_source = binascii.unhexlify(eth_address[17][0]['addr'].replace(':',''))

mac_source=binascii.unhexlify(eth_address[17][0]['addr'].replace(':',''))
print "********************Injecting ARP Packet********************"
print ""
for ip in network_range:
	
	ip_destination = socket.inet_aton(str(ip))
	#ARP packet: Initial three fields belong to ethernet packet rest is ARP, 
	#third field \x08\06 represents an ARP types of ethernet frame
        packet = struct.pack("!6s6s2s2s2s1s1s2s6s4s6s4s","\xff\xff\xff\xff\xff\xff",\
mac_source,"\x08\x06","\x00\x01","\x08\x00","\x06","\x04",\
"\x00\x01", mac_source,ip_source, "\x00\x00\x00\x00\x00\x00", ip_destination)
	#Sending the raw packet
	raw_socket.send(packet)

print "*******************Injection Completed**********************"
