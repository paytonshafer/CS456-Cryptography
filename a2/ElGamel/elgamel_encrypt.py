#python3 elgamel_encrypt.py pub.keys plain.txt encrypt.txt to run
from random import randint
import sys

pubkeys = open(sys.argv[1], 'r') #pub key file
plain = open(sys.argv[2], 'r') #plain text to be encrypted
encrypt = open(sys.argv[3], 'w') #file to write the encrypted text to

p = int(pubkeys.readline()) #prime
g = int(pubkeys.readline()) #generator
b = int(pubkeys.readline()) #public value

lines = plain.readlines()
text = ''
text = text.join(lines)

for i in text:
    alpha = randint(0, p-1) #get alpha
    h = pow(g, alpha, p) #calculate half mask
    f = pow(b, alpha, p) #calculate full mask
    c = (ord(i)*f) % p #encrypt the char
    encrypt.write(str(c) + ',' + str(h) + '\n') #write cipher to file