import sys
import base64
import struct

#Given public key file pub.key and flag.b64
#ALEXCTF{SMALL_PRIMES_ARE_BAD}
def gcd(p1, p2):
    while p1 != 0:
        p1, p2 = p2 % p1, p1
    return p2


def modInverse(p1, m):

    #Checking if p1 and M are relatively prime if not then there could be no mod inverse
    if gcd(p1, m) != 1:
        return None

    par1, par2, par3 = 1, 0, p1
    par4, par5, par6 = 0, 1, m
    while par6 != 0:
        q = par3 // par6 # // is the integer division operator
        par4, par5, par6, par1, par2, par3 = (par1 - q * par4), (par2 - q * par5), (par3 - q * par6), par4, par5, par6
    return par1 % m




# Using open ssl on file pub.key
#openssl rsa -pubin -noout -text < key.pub
#get the second field from the public key file which is modulus and first one is#encryption key
modulus=833810193564967701912362955539789451139872863794534923259743419423089229206473091408403560311191545764221310666338878019L


#Using factorDB to get the factors of modulus so we get 
p=863653476616376575308866344984576466644942572246900013156919
q=965445304326998194798282228842484732438457170595999523426901
e=65537

phi=(p-1)*(q-1)

d=modInverse(e,phi)
print "Decryption key"
print d

#flag given in flag.b64 file
flag='Ni45iH4UnXSttNuf0Oy80+G5J7tm8sBJuDNN7qfTIdEKJow4siF2cpSbP/qIWDjSi+w='
import base64

decoded=base64.b64decode(flag)

#Used rsacrack.py to do (flag^d mod modulus)
#base64 -d ./Challenges/flag.b64 | python rsacrack.py -d 33ad09ca06f50f9e90b1acae71f390d6b92f1d6d3b6614ff871181c4df08da4c5f5012457a64309405eaecd6341e43027931 52a99e249ee7cf3c0cbf963a009661772bc9cdf6e1e3fbfc6e44a07a5e0f894457a9f81c3ae132ac5683d35b28ba5c324243


print decoded
from string import *
#print atol(decoded,16)

#text=struct.unpack("!50s",decoded)
#print text

plaintext=pow(decoded,d,modulus)
#print plaintext
