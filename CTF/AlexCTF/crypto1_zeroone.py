import time
replacements = {'ZERO':'0', 'ONE':'1'}

#ALEXCTF{TH15_1S_5UP3R_5ECR3T_TXT}
with open('zero_one') as infile, open('one', 'w') as outfile:
    for line in infile:
        for src, target in replacements.iteritems():
            line = line.replace(src, target)
	    print len(line)
	   #print line.replace(' ','')
	    print "tada"
	    print len(line)
        outfile.write(line)


champ=line.decode('ascii')
print "cha"
print champ
#''.join(chr(int(line[i:i+8], 2)) for i in xrange(0, len(line), 8))
