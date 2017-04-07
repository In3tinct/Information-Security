import mechanize

#Mechanize a great tool which emulates the browser by maintaing state of the http request
object=mechanize.Browser()

object.open("http://ec2-34-207-132-244.compute-1.amazonaws.com/users/sign_in")

for form in object.forms():
	print form

#Selecting the form and providing it with username and password
object.select_form(nr=0)
object.form['user[email]']='vaibhav.agrawal0289@gmail.com'
object.form['user[password]']='test123'

#Submitting the form
object.submit()

#print object.response().read()


#Setting the values be sent
date='2017-04-07'
sessionId='3dayy6mx-khpt-17j4nkj3-6swm4a8gbtp57m2y'

#Calculating hash Mac
from hashlib import sha1
import binascii
import hmac
hashedMac=hmac.new(date, sessionId, sha1).digest()
#Converting the binary into hexadecimal
hashedMac2=binascii.hexlify(hashedMac)
print hashedMac2


#Clicking the link
level3= object.click_link(text='Level Three')
print "--------------"
#print object._ua_handlers['_cookies'].cookiejar

#Setting the headers
object.addheaders = [('X-Authorization-Date', date),
        ('X-Session-Id', sessionId),
        ('X-Signature-AllComp', hashedMac2)]

import re

while 1:

	object.open(level3)
	print object.geturl()

	#request = object.request
	#print "Header Items"
	#print request.header_items()
	#print object.response().read()

	# If the string The Password for this level is, is present(Assuming like previous challenges), that shall be the page
	# we are looking for
	count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape("The Password for this level is"), object.response().read()))
	print count
	if (count==1):
		#Printing the entire response to see the password.
		print object.response().read()
		break

print "Found"
