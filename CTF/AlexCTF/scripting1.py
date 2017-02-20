import socket
import time

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect(('195.154.53.62',1337))
#FLag ALEXCTF{1_4M_l33t_b0t}
while True:
	data=sock.recv(1024)
	if data:
		print data
		totalLines= data.count('\n')
		calculate= data.splitlines()[totalLines-1]
		#print calculate
		calculate= calculate.replace('=','')
		answer=eval(calculate)
		print str(answer)
		sock.send(str(answer)+'\r\n')
		#time.sleep(4)
	else:
		print "Closing"
		sock.close()


