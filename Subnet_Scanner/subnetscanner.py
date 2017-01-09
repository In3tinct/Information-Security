import socket
import struct
import binascii
import netifaces
#from netaddr import IPNetwork
import netaddr
import re
import thread


#Calculating the CIDR of the netmask
def calculateCIDR(networkmask):
        binary_str = ''
        for octet in networkmask:
                binary_str += bin(int(octet))[2:].zfill(8)
        return str(len(binary_str.rstrip('0')))

#Sniffing arp responses
def scanningNetwork(threadname,delay):
	#0x0003 represents all type of protocol it will listen to
	rawsock=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0003))


	# 2048 is the number of default network byte read
	while True:
		packet=rawsock.recvfrom(65565)

		#Initial 14 bytes  headers of ethernet frames
		ethHeader=packet[0][0:14]

		# exclamation represents network byte order, 6s6s2s, 6s is for 6 short bytes and so on
		ethHeaderValues=struct.unpack('!6s6sH',ethHeader)
		#It shall give 8 for IP protocol, we have to use 6s6sH above
	
		typeOfProtocol=socket.ntohs(ethHeaderValues[2])
	
		#IP packet type is 0x0800. You use 8 because you displayed it in the network byte order (use ntohs() to convert it).
		#All packet types are defined in include/linux/if_ether.h
		#1544 is in fact 0x0806 = ARP	
		if typeOfProtocol==1544:
			arp = packet[0][14:42]
	    		arp_header = struct.unpack("2s2s1s1s2s6s4s6s4s", arp)
			arp_op_code=binascii.hexlify(arp_header[4])
			if arp_op_code=='0002':
				print "Host is up:"
				print socket.inet_ntoa(arp_header[6])



#########Main method

if __name__ == "__main__":
	#Creating a thread for listening the reply ARP packets on the raw socket
	try:
	   	thread.start_new_thread( scanningNetwork, ("Thread-1", 2, ) )	
	except:
   		print "Error: unable to start thread"

	#Injecting ARP packets
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
	print "********************Injecting the packet********************"

	for ip in network_range:
	
		ip_destination = socket.inet_aton(str(ip))
		#ARP packet: Initial three fields belong to ethernet packet rest is ARP, 
		#third field \x08\06 represents an ARP types of ethernet frame
		packet = struct.pack("!6s6s2s2s2s1s1s2s6s4s6s4s","\xff\xff\xff\xff\xff\xff",\
	mac_source,"\x08\x06","\x00\x01","\x08\x00","\x06","\x04",\
	"\x00\x01", mac_source,ip_source, "\x00\x00\x00\x00\x00\x00", ip_destination)
		raw_socket.send(packet)	


	print "******************Packet Injection Completed******************"
	print "Printing the responses"
	#Keep running the main thread, Because a child thread if listening for the 
	#ARP replies
	while 1:
		pass

