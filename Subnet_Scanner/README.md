A local subnet scanner it checks for all the host which
are up, by sending the ARP request and checking what all hosts sends ARP reply back.

Default interface used is eth0

Environment: Linux

Programming langugage: Python

One program uses Scapy library While the other program uses Raw Sockets only(Needs a bit of refinement, responses differ sometimes)
Libraries: Scapy, Netifaces, Netaddr
