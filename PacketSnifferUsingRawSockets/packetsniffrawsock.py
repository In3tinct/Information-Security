import socket
import struct
import binascii

#0x0800 represents internet protocol
rawsock=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))

# 2048 is the number of default network byte read
while True:
	packet=rawsock.recvfrom(65565)
	print len(packet[0])

	print "------------------Start of packet-------------------"
	print "Raw Socket:"
	print packet

	#Initial 14 bytes  headers of ethernet frames
	ethHeader=packet[0][0:14]

	# exclamation represents network byte order, 6s6s2s, 6s is for 6 short bytes and so on
	ethHeaderValues=struct.unpack('!6s6sH',ethHeader)

	#It shall give 8 for IP protocol, we have to use 6s6sH above
	typeOfProtocol=socket.ntohs(ethHeaderValues[2])

	print "Type of Protocol:%i"%typeOfProtocol

	destinationMAC=ethHeaderValues[0]
	sourceMAC=ethHeaderValues[1]

	print "destination MAC:%s"%binascii.hexlify(destinationMAC)
	print "source MAC:%s"%binascii.hexlify(sourceMAC)

	#If IP protocol
	if typeOfProtocol==8:
		#After the ethernet frames, 20 bytes header of IP packet
		ipHeader=packet[0][14:34]
		ipHeaderValues=struct.unpack('!BBHHHBBH4s4s',ipHeader)
		
		protocol=ipHeaderValues[6]
		sourceIp=ipHeaderValues[8]
		destinationIp=ipHeaderValues[9]
		
		print "Source IP: %s"%socket.inet_ntoa(sourceIp)
		print "Destination IP: %s"%socket.inet_ntoa(destinationIp)

		#After IP packets, 20 bytes header of TCP segments
		if protocol==6:
			tcpHeader=packet[0][34:54]
			tcpHeaderValues=struct.unpack('!HH16s',tcpHeader)
			
			print "TCP Source port:%i"%tcpHeaderValues[0]
			print "TCP Destination port:%i"%tcpHeaderValues[1]
			
			#Checking only for incoming packets
			if tcpHeaderValues[0] in (443,80):
				if tcpHeaderValues[0]==80:
					print "HTTP Traffic"
				else:
					print "HTTPS Traffic"
				httpsHeaderAndData=packet[0][54:]
				print len(httpsHeaderAndData)
				length=len(httpsHeaderAndData)
				l=[]
				l.append('!')
				#Subtracted 2 from length because binascii.hexlify was getting the data as a tuple %02%02,) after unpacking,
				#So we ignored the last two bytes
				l.append(str(length-2))
				l.append('s')
				l.append('2')
				l.append('s')
				regex=''.join(l)
				print regex
				if length!=0:
					data=struct.unpack(regex,httpsHeaderAndData)
					print data
					print binascii.hexlify(data[0])
		elif protocol==17:
			udpHeader=packet[0][34:42]
			udpHeaderValues=struct.unpack('!HHHH',udpHeader)
		
			print "UDP Source port:%s" %str(udpHeaderValues[0])
			print "UDP Destination port:%s" %str(udpHeaderValues[1])
#httpHeader=packet[0][54:300]
#print struct.unpack('!246s',httpHeader)
