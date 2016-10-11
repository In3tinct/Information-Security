import base64
import sys

#Modulus N
#N=402394248802762560784459411647796431108620322919897426002417858465984510150839043308712123310510922610690378085519407742502585978563438101321191019034005392771936629869360205383247721026151449660543966528254014636648532640397857580791648563954248342700568953634713286153354659774351731627683020456167612375777

#Public key exponent for first user
#e1=3

#Public key exponent for second user 0x10001
#e2=65537

#First Ciphertext 
#c1=239450055536579126410433057119955568243208878037441558052345538060429910227864196906345427754000499641521575512944473380047865623679664401229365345208068050995600248796358129950676950842724758743044543343426938845678892776396315240898265648919893384723100132425351735921836372375270138768751862889295179915967

#Second Ciphertext
#c2=138372640918712441635048432796183745163164033759933692015738688043514876808030419408866658926149572619049975479533518038543123781439635367988204599740411304464710538234675409552954543439980522243416932759834006973717964032712098473752496471182275216438174279723470286674311474283278293265668947915374771552561


def xgcd(a,b):
	if b == 0:
	 return [1,0,a]
	else:
	 x,y,d = xgcd(b, a%b)
	 return [y, x - (a//b)*y, d]


def gcd(a, b):
    # Return the GCD of a and b using Euclid's Algorithm
    while a != 0:
        a, b = b % a, a
    return b

#c2 would be a and Modulus N would be m
def modInverse(a, m):

    if gcd(a, m) != 1:
        return None # no mod inverse if a & m aren't relatively prime

    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m




def main():
	if len(sys.argv) < 6:
		print("Insufficient parameters, Please provide parameters in order of N,e1,e2,c1,c2")
		return
	
        N=long(sys.argv[1])
	e1=long(sys.argv[2])
	e2=long(sys.argv[3])
	c1=long(sys.argv[4])
	c2=long(sys.argv[5])
	
	euclidConstants=xgcd(e1,e2)
	a=euclidConstants[0]	
	b=euclidConstants[1]

	eq1=modInverse(c2,N)


	#(c1^a * eq1^-b) mod N
	result1=pow(eq1,-b,N)
	result2=pow(c1,a,N)

	result3=result1*result2
	finalresult=result3%N
	#print finalresult

	hexresult=hex(finalresult)[2:-1]
	#print hexresult

	hextoascii=str(hexresult).decode("hex")
	#print hextoascii

	secretmessage=base64.b64decode(hextoascii)
	print ("The hidden message is in german, We can use google translate ;)",secretmessage) 

if __name__ == "__main__":
    	main()


