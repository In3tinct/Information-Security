comeon=[]

def convert_to_ascii(text):
    return "".join(str(ord(char)) for char in text)
length=0
with open('./Challenges/msg') as file:
	for f in file:
		f=f[:-1]
		#print f
		#print len(f)	
		comeon.append(f)
comeoneCopy=comeon
xoredCipherText=[]
from binascii import unhexlify, hexlify
for data in comeon:
	for data1 in comeoneCopy:
		#data=hex(data)
		#data1=hex(data1)
		s1=data
		s2=data1
		#print s1
		#print s2 
		xored= hexlify(''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(unhexlify(s1[-len(s2):]), unhexlify(s2))))
		#print xored
		xoredCipherText.append(xored)
	break;	
print "-----------------Round completed----------------"

del xoredCipherText[0]

#Guessing the word "the"

guessHex=hexlify(b'Dear Friend')

count=0

#First taking out all the xored cipher text and trying to xor it with guess word
#and then cribbing it on the next position of the cipher text xor and so on

#First position and then so on
for i in range(0,15):
	#Iterating over the xors of cipher text
	for j in xoredCipherText:
		print j
		#Trimming the xor of cipher text(which becomes XOR of plaintext as well)
		#to the size of the word we are using for crib dragging
		j=j[i:(len(guessHex)+i)]
		print j
		print guessHex
	 
		xoredWithGuess= hexlify(''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(unhexlify(j[-len(guessHex):]), unhexlify(guessHex))))
		#Converting the hex to its ascii value 
		
		
		print xoredWithGuess
		hextoascii=str(xoredWithGuess).decode("hex")
		
		print hextoascii
		print "-------------------------------------"
	break
