from sys import argv
import binascii
from itertools import product
script, fn, opt = argv

#input is script, filename, and either 10-byte key, or 'brute' to initiate brute force decryption. 
#the only rig keys i have seen thus far have been 'gexywoaxor', so that should work for the most part.

def filewrite(fn):
	#checks input for either brute option or key data
	if opt=='brute':
		brute()
	else:
		i=decode(fn, opt)
	z=0
	decoded=open('output.mal','wb')
	while z<len(i):
		#decoded=open('output.mal','wb')
		#Weird hacky line to unhexlify ords into hex without the '0x' prefix.
		#Other ideas welcome
		decoded.write(binascii.unhexlify(binascii.hexlify(chr(int(i[z])))))
		z+=1

def decode(fn, k):
	#takes filename and key args.
	filename = fn
	key=k
	b=[0]*256
	a=0
	r=255
	keylen=len(key)
	c=d=a=0
	encoded=bytearray(open(filename, 'rb').read())
	print "Encoded file of length %s" % len(encoded)
	#declaring array of file length
	i=[0]*len(encoded)
	#loop to create key value array where index num. == value at index
	while a<r+1:
		b[a]=a
		a+=1
	a=0
	while r+1>a:
		c=c+b[a]+(ord(key[a%keylen]))&255
		d=b[a]
		b[a]=b[c]
		b[c]=d
		a+=1
	e=c=a=0
	while e<len(encoded):
		a=a+1&r
		c=c+b[a]&r
		d=b[a]
		b[a]=b[c]
		b[c]=d
		#final xor to add to i decoded array
		i[e]=encoded[e]^b[b[a]+(b[c])&r]
		#checks decoded bytes after third iteration for 'MZ' file header. breaks otherwise. should save a lot of time on brute force.
		if (e==3 and i[0]==77 and i[1]==90):
			print "\n\nFile header 'MZ'. It probably worked! Key is %s\n\n" % k
			e+=1
			continue
		elif (e==3 and i[0]!=77 and i[1]!=90):
			break
		else:
			e+=1
			continue
		e+=1
	print "Decoded output of length %s" % len(i)
	return i
def brute():
	#brute force decryption. still runs values less than 10 bytes. need to fix.
	chars='abcdefghijklmnopqrstuvwxyz'
	for length in range(10): # only do lengths of 1 + 2
		to_attempt = product(chars, repeat=length)
		for attempt in to_attempt:
			if len(attempt)==10:
				decode(fn, ''.join(attempt))
			else:
				pass
filewrite(fn)
